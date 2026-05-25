using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Text;
using System.Web.Script.Serialization;

namespace MobileSmartsSyntaxChecker
{
    internal static class Program
    {
        private const string DefaultMobileSmartsDir = @"E:\MobileSmarts\Desktop";
        private const string DefaultServerBinDir = @"E:\MobileSmarts\Server\DataService\Bin";

        private static readonly List<string> ResolveDirectories = new List<string>();

        private static int Main(string[] args)
        {
            Console.InputEncoding = Encoding.UTF8;
            Console.OutputEncoding = Encoding.UTF8;

            CheckerRequest request;

            try
            {
                request = ParseRequest(args);
                ConfigureAssemblyResolve(request.MobileSmartsDir);

                ValidationResult result = Validate(request);
                Console.WriteLine(ToJson(result));
                return result.Ok ? 0 : 2;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ToJson(ValidationResult.FromException("fatal", null, ex)));
                return 1;
            }
        }

        private static CheckerRequest ParseRequest(string[] args)
        {
            Dictionary<string, string> values = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

            for (int i = 0; i < args.Length; i++)
            {
                string arg = args[i];
                if (arg == "--stdin")
                {
                    string json = Console.In.ReadToEnd();
                    return ParseJsonRequest(json);
                }

                if (!arg.StartsWith("--", StringComparison.Ordinal))
                    continue;

                string key = arg.Substring(2);
                string value = "true";
                if (i + 1 < args.Length && !args[i + 1].StartsWith("--", StringComparison.Ordinal))
                    value = args[++i];
                values[key] = value;
            }

            CheckerRequest request = new CheckerRequest();
            request.Mode = GetValue(values, "mode", "expression");
            request.MobileSmartsDir = GetValue(values, "mobile-smarts-dir", DefaultMobileSmartsDir);
            request.NormalizeBraces = !StringEquals(GetValue(values, "normalize-braces", "true"), "false");

            string sourceFile = GetValue(values, "source-file", null);
            if (!string.IsNullOrEmpty(sourceFile))
                request.Source = File.ReadAllText(sourceFile, Encoding.UTF8);
            else
                request.Source = GetValue(values, "source", null);

            if (request.Source == null)
                throw new ArgumentException("Source is required. Use --source, --source-file, or --stdin.");

            return request;
        }

        private static CheckerRequest ParseJsonRequest(string json)
        {
            if (string.IsNullOrWhiteSpace(json))
                throw new ArgumentException("Empty stdin JSON.");

            JavaScriptSerializer serializer = new JavaScriptSerializer();
            Dictionary<string, object> obj = serializer.Deserialize<Dictionary<string, object>>(json);

            CheckerRequest request = new CheckerRequest();
            request.Mode = GetJsonString(obj, "mode", "expression");
            request.Source = GetJsonString(obj, "source", null);
            request.MobileSmartsDir = GetJsonString(obj, "mobileSmartsDir", DefaultMobileSmartsDir);
            object normalizeObj;
            request.NormalizeBraces = !obj.TryGetValue("normalizeBraces", out normalizeObj) || Convert.ToBoolean(normalizeObj);

            string sourceFile = GetJsonString(obj, "sourceFile", null);
            if (request.Source == null && !string.IsNullOrEmpty(sourceFile))
                request.Source = File.ReadAllText(sourceFile, Encoding.UTF8);

            if (request.Source == null)
                throw new ArgumentException("JSON field 'source' or 'sourceFile' is required.");

            return request;
        }

        private static ValidationResult Validate(CheckerRequest request)
        {
            string mode = (request.Mode ?? "expression").Trim().ToLowerInvariant();
            string source = request.Source ?? string.Empty;
            string normalized = NormalizeSource(mode, source, request.NormalizeBraces);

            try
            {
                Assembly parsingAssembly = LoadParsingAssembly(request.MobileSmartsDir);

                switch (mode)
                {
                    case "expression":
                    case "expr":
                        CompileExpression(parsingAssembly, normalized);
                        break;

                    case "template":
                    case "tmpl":
                        ParseWithParserProperty(parsingAssembly, "TemplatesParser", source);
                        break;

                    case "code":
                        CompileCode(parsingAssembly, source);
                        break;

                    case "auto":
                        ValidateAuto(parsingAssembly, source, normalized);
                        break;

                    default:
                        throw new ArgumentException("Unknown mode '" + request.Mode + "'. Supported modes: expression, template, code, auto.");
                }

                return ValidationResult.Success(mode, normalized);
            }
            catch (TargetInvocationException ex)
            {
                return ValidationResult.FromException(mode, normalized, ex.InnerException ?? ex);
            }
            catch (Exception ex)
            {
                return ValidationResult.FromException(mode, normalized, ex);
            }
        }

        private static void ValidateAuto(Assembly parsingAssembly, string source, string normalizedExpression)
        {
            Exception expressionError = null;
            try
            {
                CompileExpression(parsingAssembly, normalizedExpression);
                return;
            }
            catch (TargetInvocationException ex)
            {
                expressionError = ex.InnerException ?? ex;
            }
            catch (Exception ex)
            {
                expressionError = ex;
            }

            try
            {
                ParseWithParserProperty(parsingAssembly, "TemplatesParser", source);
                return;
            }
            catch
            {
                // Preserve the expression error because it is usually the most useful for action attributes.
                throw expressionError;
            }
        }

        private static string NormalizeSource(string mode, string source, bool normalizeBraces)
        {
            if (!normalizeBraces)
                return source;

            if (StringEquals(mode, "expression") || StringEquals(mode, "expr") || StringEquals(mode, "auto"))
                return source == null ? null : source.Trim().TrimStart('{').TrimEnd('}');

            return source;
        }

        private static Assembly LoadParsingAssembly(string mobileSmartsDir)
        {
            string baseDir = string.IsNullOrWhiteSpace(mobileSmartsDir) ? DefaultMobileSmartsDir : mobileSmartsDir;
            string parsingPath = Path.Combine(baseDir, "Cleverence.Parsing.dll");

            if (!File.Exists(parsingPath))
            {
                parsingPath = Path.Combine(DefaultMobileSmartsDir, "Cleverence.Parsing.dll");
                if (!File.Exists(parsingPath))
                    parsingPath = Path.Combine(DefaultServerBinDir, "Cleverence.Parsing.dll");
            }

            if (!File.Exists(parsingPath))
                throw new FileNotFoundException("Cleverence.Parsing.dll was not found.", parsingPath);

            AddResolveDirectory(Path.GetDirectoryName(parsingPath));
            AddResolveDirectory(DefaultMobileSmartsDir);
            AddResolveDirectory(DefaultServerBinDir);

            return Assembly.LoadFrom(parsingPath);
        }

        private static void ConfigureAssemblyResolve(string mobileSmartsDir)
        {
            AddResolveDirectory(AppDomain.CurrentDomain.BaseDirectory);
            AddResolveDirectory(mobileSmartsDir);
            AddResolveDirectory(DefaultMobileSmartsDir);
            AddResolveDirectory(DefaultServerBinDir);

            AppDomain.CurrentDomain.AssemblyResolve += ResolveAssembly;
        }

        private static Assembly ResolveAssembly(object sender, ResolveEventArgs args)
        {
            string simpleName = new AssemblyName(args.Name).Name + ".dll";
            foreach (string directory in ResolveDirectories)
            {
                if (string.IsNullOrWhiteSpace(directory))
                    continue;

                string candidate = Path.Combine(directory, simpleName);
                if (File.Exists(candidate))
                    return Assembly.LoadFrom(candidate);
            }

            return null;
        }

        private static void AddResolveDirectory(string directory)
        {
            if (string.IsNullOrWhiteSpace(directory))
                return;

            string fullPath = Path.GetFullPath(directory);
            if (!ResolveDirectories.Contains(fullPath))
                ResolveDirectories.Add(fullPath);
        }

        private static void CompileExpression(Assembly parsingAssembly, string source)
        {
            Type type = parsingAssembly.GetType("Cleverence.Parsing.CompiledExpression", true);
            MethodInfo method = type.GetMethod("Compile", BindingFlags.Public | BindingFlags.Static, null, new[] { typeof(string) }, null);
            method.Invoke(null, new object[] { source });
        }

        private static void CompileCode(Assembly parsingAssembly, string source)
        {
            Type type = parsingAssembly.GetType("Cleverence.Parsing.CompiledCode", true);
            MethodInfo method = type.GetMethod("Compile", BindingFlags.Public | BindingFlags.Static, null, new[] { typeof(string) }, null);
            method.Invoke(null, new object[] { source });
        }

        private static void ParseWithParserProperty(Assembly parsingAssembly, string propertyName, string source)
        {
            Type parsersType = parsingAssembly.GetType("Cleverence.Parsing.Parsers", true);
            PropertyInfo property = parsersType.GetProperty(propertyName, BindingFlags.Public | BindingFlags.Static);
            object parser = property.GetValue(null, null);
            MethodInfo parse = parser.GetType().GetMethod("Parse", BindingFlags.Public | BindingFlags.Instance, null, new[] { typeof(string) }, null);
            parse.Invoke(parser, new object[] { source });
        }

        private static string GetValue(Dictionary<string, string> values, string key, string defaultValue)
        {
            string value;
            return values.TryGetValue(key, out value) ? value : defaultValue;
        }

        private static string GetJsonString(Dictionary<string, object> values, string key, string defaultValue)
        {
            object value;
            return values.TryGetValue(key, out value) && value != null ? Convert.ToString(value) : defaultValue;
        }

        private static bool StringEquals(string left, string right)
        {
            return string.Equals(left, right, StringComparison.OrdinalIgnoreCase);
        }

        private static string ToJson(ValidationResult result)
        {
            JavaScriptSerializer serializer = new JavaScriptSerializer();
            return serializer.Serialize(result);
        }
    }

    internal sealed class CheckerRequest
    {
        public string Mode;
        public string Source;
        public string MobileSmartsDir;
        public bool NormalizeBraces = true;
    }

    public sealed class ValidationResult
    {
        public bool Ok { get; set; }
        public string Mode { get; set; }
        public string Normalized { get; set; }
        public List<ValidationError> Errors { get; set; }

        public static ValidationResult Success(string mode, string normalized)
        {
            return new ValidationResult
            {
                Ok = true,
                Mode = mode,
                Normalized = normalized,
                Errors = new List<ValidationError>()
            };
        }

        public static ValidationResult FromException(string mode, string normalized, Exception ex)
        {
            ValidationError error = new ValidationError
            {
                Type = ex.GetType().FullName,
                Message = ex.Message,
                Details = ex.ToString()
            };

            return new ValidationResult
            {
                Ok = false,
                Mode = mode,
                Normalized = normalized,
                Errors = new List<ValidationError> { error }
            };
        }
    }

    public sealed class ValidationError
    {
        public string Type { get; set; }
        public string Message { get; set; }
        public string Details { get; set; }
    }
}
