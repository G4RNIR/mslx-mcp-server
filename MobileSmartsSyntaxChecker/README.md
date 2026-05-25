# MobileSmartsSyntaxChecker

CLI-проверка синтаксиса Mobile SMARTS через родную `Cleverence.Parsing.dll`.

MCP-сервер вызывает этот exe из `validate_mslx_syntax` и из pre-flight проверок перед записью `expression`, `template`, `code` и некоторых вложенных значений.

## Требования

- Windows.
- .NET Framework compiler `csc.exe`:
  - `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe`
  - или `C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe`
- Установленный Mobile SMARTS с файлом `Cleverence.Parsing.dll`.

По умолчанию checker ищет `Cleverence.Parsing.dll` здесь:

```text
E:\MobileSmarts\Desktop
E:\MobileSmarts\Server\DataService\Bin
```

Другой путь можно передать параметром `--mobile-smarts-dir` или через MCP-переменную окружения `MOBILESMARTS_DIR`.

## Сборка

Из корня проекта:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\MobileSmartsSyntaxChecker\build.ps1
```

Результат:

```text
MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe
```

## Режимы

- `expression` - `CompiledExpression.Compile(...)`
- `template` - `Parsers.TemplatesParser.Parse(...)`
- `code` - `CompiledCode.Compile(...)`
- `auto` - сначала `expression`, затем `template`

## Примеры

```powershell
.\MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe --mode expression --source "global::System.String.IsNullOrEmpty(Document.Number) == false"
```

```powershell
.\MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe --mode expression --source "SelectedLine.номер"
```

```powershell
.\MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe --mode template --source "Документ {Document.Name}"
```

Для длинных выражений:

```powershell
.\MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe --mode expression --source-file E:\tmp\expr.txt
```

JSON через stdin:

```powershell
'{"mode":"expression","source":"SelectedLine.Quantity > 0"}' |
  .\MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe --stdin
```

JSON через stdin с русскими идентификаторами лучше передавать в UTF-8 или через `\uXXXX` escape.

## Коды выхода

- `0` - синтаксис корректен
- `2` - ошибка синтаксиса/компиляции
- `1` - фатальная ошибка checker-а
