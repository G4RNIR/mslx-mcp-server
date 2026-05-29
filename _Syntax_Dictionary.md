# 📚 Расширенный словарь синтаксиса Mobile SMARTS

> **ВАЖНО ДЛЯ ИИ-АГЕНТА:** Этот файл содержит реально используемый синтаксис проприетарной платформы. При написании кода строго сверяйся с этими вызовами. Не выдумывай методы C#, используй только то, что есть здесь.

## 1. Global (Системные функции)

### `global::Cleverence.Barcoding.Ean128.AutoFormatEnabled`
**Примеры из базы:**
```csharp
global::Cleverence.Barcoding.Ean128.AutoFormatEnabled = true;
```
```csharp
ScannedBarcode.Length >= 24 && global::Cleverence.Barcoding.Ean128.AutoFormatEnabled
```
```csharp
temp = global::Cleverence.Barcoding.Ean128.AutoFormatEnabled; global::Cleverence.Barcoding.Ean128.AutoFormatEnabled = true;
```
```csharp
global::Cleverence.Barcoding.Ean128.AutoFormatEnabled = temp
```

### `global::Cleverence.Barcoding.Ean128.FormatAnyway`
**Примеры из базы:**
```csharp
temp = global::Cleverence.Barcoding.Ean128.FormatAnyway(ScannedBarcode); ScannedBarcode = temp != empty?temp:ScannedBarcode; Коды = global::Clevere...
```

### `global::Cleverence.MOTP.Utils.GetMRP`
**Примеры из базы:**
```csharp
encoded = BarcodeData.ScannedBarcodeCompatible.Substring(21, 4); PricePerUnit = global::Cleverence.MOTP.Utils.GetMRP(encoded);
```

### `global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell`
**Примеры из базы:**
```csharp
Ячейка = global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell(ПолеПоиска); CellName = Ячейка;
```
```csharp
if (FirstStorage == null && СтрокиОстатков[0].ИдЯчейки != "") FirstStorage = global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell(СтрокиОстатк...
```
```csharp
Ячейка = global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell(BarcodeData.BarcodeRaw); ЭтоЯчейка = Ячейка != null;
```

### `global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet`
**Примеры из базы:**
```csharp
if (BarcodeData != null) { if (BarcodeData.IsGS1Compatible) Barcode = BarcodeData.BarcodeGS1Formatted; else Barcode = BarcodeData.BarcodeRaw; Транс...
```
```csharp
temp = global::Cleverence.Barcoding.Ean128.FormatAnyway(ScannedBarcode); ScannedBarcode = temp != empty?temp:ScannedBarcode; Коды = global::Clevere...
```
```csharp
ТУ = global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet(BarcodeData.BarcodeRaw); if (ТУ != null && ТУ.ЭтоБлок == false) ТУ == null;
```
```csharp
pal = global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet(bd.BarcodeRaw);
```
```csharp
SSCCPallet = global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet(bd.BarcodeRaw);
```

### `global::Cleverence.Warehouse.Compact.AdvancedOps.PackProduct`
**Примеры из базы:**
```csharp
SelectedProduct = global::Cleverence.Warehouse.Compact.AdvancedOps.PackProduct(СтрокаКМОстатки.ИдТовара, СтрокаКМОстатки.ИдЕдиницыИзмерения)
```
```csharp
if (ВыборПоМарке.ИдТовара != "" && ВыборПоМарке.ИдЕдиницыИзмерения != "") SelectedProduct = global::Cleverence.Warehouse.Compact.AdvancedOps.PackPr...
```

### `global::Cleverence.Warehouse.DeviceInfo.GeneralFields`
**Примеры из базы:**
```csharp
global::Cleverence.Warehouse.DeviceInfo.GeneralFields["ИдУзла"] = ""
```
```csharp
GlobalVars.ИдУзла = ДоступныеУзлы[0].Ид; global::Cleverence.Warehouse.DeviceInfo.GeneralFields["ИдУзла"] = ДоступныеУзлы[0].Ид;
```
```csharp
GlobalVars.ИдУзла = SelectedItem == null ? "" : SelectedItem.Ид; global::Cleverence.Warehouse.DeviceInfo.GeneralFields["ИдУзла"] = GlobalVars.ИдУзла;
```
```csharp
global::Cleverence.Warehouse.DeviceInfo.GeneralFields["ИдУзла"] = GlobalVars.ИдУзла
```

### `global::Cleverence.Warehouse.ProductsManager.AddToCache`
**Примеры из базы:**
```csharp
global::Cleverence.Warehouse.ProductsManager.AddToCache(SelectedProduct)
```

### `global::Cleverence.Warehouse.ProductsManager.FindById`
**Примеры из базы:**
```csharp
ТоварОтбор = global::Cleverence.Warehouse.ProductsManager.FindById(SelectedLine.ИдТовара)
```

### `global::Cleverence.Warehouse.ProductsManager.FindPackingById`
**Примеры из базы:**
```csharp
УпакОтбор = global::Cleverence.Warehouse.ProductsManager.FindPackingById(SelectedLine.ИдТовара, SelectedLine.ИдЕдиницыИзмерения)
```

### `global::System.Char.IsControl`
**Примеры из базы:**
```csharp
Разделитель = Barcode.Substring(31, 1); if (global::System.Char.IsControl(Barcode, 31) || Разделитель == FNC1) КМ = Barcode.Replace(Разделитель, "");
```
```csharp
Разделитель = Barcode.Substring(25, 1); if (global::System.Char.IsControl(Barcode, 25) || Разделитель == FNC1) КМ = Barcode.Replace(Разделитель, "");
```

### `global::System.Char.IsDigit`
**Примеры из базы:**
```csharp
while (idx < sub1.Length) { if (global::System.Char.IsDigit(sub1, idx) == false) hasChar = true; idx = idx + 1; }
```

### `global::System.Convert.ToChar`
**Примеры из базы:**
```csharp
GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString(); ДатаСкана = CurrentDate;
```
```csharp
GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString();
```
```csharp
SavedBarcode = Barcode; GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString(); BarcodeData = GO.G...
```
```csharp
GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString(); Иероглиф = global::System.Convert.ToChar(3...
```
```csharp
GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString(); NewLine = global::System.Environment.NewLi...
```

### `global::System.Decimal.Parse`
**Примеры из базы:**
```csharp
ИнтАлкоСН = global::System.Decimal.Parse(SelectedProduct.АлкоСН)
```

### `global::System.Double.Parse`
**Примеры из базы:**
```csharp
height = global::System.Double.Parse(GlobalVars.ВысотаЭтикетки)
```
```csharp
length = global::System.Double.Parse(GlobalVars.ШиринаЭтикетки)
```

### `global::System.Environment.NewLine`
**Примеры из базы:**
```csharp
GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString(); NewLine = global::System.Environment.NewLi...
```

### `global::System.Guid.NewGuid`
**Примеры из базы:**
```csharp
Серия.Ид = global::System.Guid.NewGuid().ToString()
```

### `global::System.Int32.Parse`
**Примеры из базы:**
```csharp
First=global::System.Int32.Parse(FirstSerial.Substring(SerialPrefixLength))
```
```csharp
Last=global::System.Int32.Parse(LastSerial.Substring(SerialPrefixLength))
```
```csharp
Contrast = global::System.Int32.Parse(GlobalVars.Contrast)
```

## 3. Document (Шапка документа)

### `Document.Barcode`
**Примеры из базы:**
```csharp
Document.Barcode != ""
```
```csharp
Document.Barcode = Result
```
```csharp
Document.Barcode = ScannedBarcode
```

### `Document.Completed`
**Примеры из базы:**
```csharp
Document.КонтрольКолва == 1 && Document.Completed &&СтрокиТоваровДляПроставления.Count==0
```
```csharp
(КонтрольКолва == true || Document.КонтрольКолва == 1) && Document.Completed == true && СессияРежимРаботыПоЯчейкам != "после товара"
```
```csharp
Document.Completed || РазрешитьЗавершениеПоНедобору == true
```
```csharp
РазрешитьЗавершениеНесобранногоДокумента = (Document.DocumentTypeName == "ПриходНаСклад" && (GlobalVars.ЗапретитьЗавершениеНесобранногоДокументаПри...
```
```csharp
Document.Completed
```

### `Document.Contains`
**Примеры из базы:**
```csharp
Document.Contains("ПриниматьЧужиеКМ") == false || Document.ПриниматьЧужиеКМ == false
```
```csharp
СессияПерваяЯчейка = FirstStorage; if (Document.Contains("СобиратьРоссыпью")) Document.СобиратьРоссыпью = false;
```
```csharp
if (Document.Contains("СобиратьРоссыпью")) Document.СобиратьРоссыпью = false; Barcode = BarcodeData.IsGS1Compatible ? BarcodeData.BarcodeGS1Formatt...
```

### `Document.ContainsField`
**Примеры из базы:**
```csharp
if (Document.ContainsField("ПоЯчейкам")) Document.ПоЯчейкам = СессияРежимЯчеек; if (Document.ContainsField("КонтрольЯчеек")) Document.КонтрольЯчеек...
```
```csharp
if (Document.ContainsField("МестоПоискаСодержимого") && Document.МестоПоискаСодержимого == "") Document.МестоПоискаСодержимого == МестоПоискаСодерж...
```
```csharp
if (Document.ContainsField("НастройкиСохранены")) Document.НастройкиСохранены = true;
```

### `Document.ContainsMC`
**Примеры из базы:**
```csharp
SelectedProduct.Марка != "" && Document.ContainsMC
```
```csharp
src = select first (*) from Document.CurrentItems where Item.Марка != ""; Document.ContainsMC = src != null;
```

### `Document.CreatedOnPDA`
**Примеры из базы:**
```csharp
Document.CreatedOnPDA
```
```csharp
Склад.Адресный == true && Document.CreatedOnPDA && GlobalVars.РежимЯчейки[Document.DocumentType.Name] == false
```
```csharp
Склад.Адресный == false && Document.CreatedOnPDA && GlobalVars.РежимЯчейки[Document.DocumentType.Name] == true
```
```csharp
Document.CreatedOnPDA == true
```
```csharp
if(Document.CreatedOnPDA == false) Document.ПоЯчейкам = True; else { GlobalVars.РежимРаботыПоЯчейкам[Document.DocumentType.Name] = "перед товаром";...
```

### `Document.CurrentItems`
**Примеры из базы:**
```csharp
if (ЭтоТУ == true) строкиНаУдаление = select (*) from Document.CurrentItems where Item.SSCC == Barcode;
```
```csharp
if (ЭтоБлок == true) строкиНаУдаление = select (*) from Document.CurrentItems where Item.ГрупповаяУпаковка == Barcode || Item.ГрупповаяУпаковка == ...
```
```csharp
CurrentItem = select first (*) from Document.CurrentItems where Item.ОснШК == SelectedProduct.ОснШК && Item.СН == SelectedProduct.СН
```
```csharp
if (Document.ServerHosted) CurrentItem = select first (*) from Document.CurrentItems where Item.Uid == CurrentItem.Uid; DeclaredItem = CurrentItem....
```
```csharp
CurrentItems = select (*) from Document.CurrentItems where Item.ШтрихкодУпаковочногоЛиста == BarcodeData.ScannedBarcodeCompatible
```

### `Document.CurrentItems.AddRange`
**Примеры из базы:**
```csharp
Document.CurrentItems.Clear(); currentItems.CreatedBy = CreatedBy; Document.CurrentItems.AddRange(currentItems);
```

### `Document.CurrentItems.BindingKey`
**Примеры из базы:**
```csharp
Document.CurrentItems.BindingKey = ""; Document.DeclaredItems.BindingKey = "";
```

### `Document.CurrentItems.Clear`
**Примеры из базы:**
```csharp
Document.CurrentItems.Clear(); currentItems.CreatedBy = CreatedBy; Document.CurrentItems.AddRange(currentItems);
```

### `Document.CurrentItems.Count`
**Примеры из базы:**
```csharp
Document.CurrentItems.Count == 0
```
```csharp
GlobalVars.СПалетами == "ТолькоПалеты" && Document.CurrentItems.Count != 0
```
```csharp
Document.CurrentItems.Count != 0
```

### `Document.CurrentItems.CurrentQuantity`
**Примеры из базы:**
```csharp
if (CurrentItem.SSCC != ""){ ParentRow = select first (*) from Document.ТранспортныеУпаковкиФакт where Item.ШтрихкодТУ == CurrentItem.SSCC; if (Par...
```
```csharp
Document.CreatedOnPDA && Document.НастройкиСохранены == null && Document.CurrentItems.CurrentQuantity > 0
```

### `Document.DeclaredItems`
**Примеры из базы:**
```csharp
if (SelectedProduct.МаркаИСМП != "") DeclaredItem = select first (*) from Document.DeclaredItems where Item.МаркаИСМП == SelectedProduct.МаркаИСМП;...
```
```csharp
col = select (*) from Document.DeclaredItems
```
```csharp
DeclaredItems = select (FirstStorageId) from Document.DeclaredItems group by FirstStorageId
```
```csharp
DeclaredItems= select (SecondStorageId) from Document.DeclaredItems group by SecondStorageId
```
```csharp
DeclaredItems = select (SSCC) from Document.DeclaredItems group by SSCC
```

### `Document.DeclaredItems.AddRange`
**Примеры из базы:**
```csharp
Document.DeclaredItems.Clear(); Document.DeclaredItems.AddRange(declaredItems);
```

### `Document.DeclaredItems.BindingKey`
**Примеры из базы:**
```csharp
Document.CurrentItems.BindingKey = ""; Document.DeclaredItems.BindingKey = "";
```

### `Document.DeclaredItems.Clear`
**Примеры из базы:**
```csharp
Document.DeclaredItems.Clear(); Document.DeclaredItems.AddRange(declaredItems);
```

### `Document.DeclaredItems.Count`
**Примеры из базы:**
```csharp
Document.DeclaredItems.Count == 0
```
```csharp
Document.DeclaredItems.Count > 0
```

### `Document.DeclaredItems.FindByFirstCellIdWithCommon`
**Примеры из базы:**
```csharp
СтрокиТовараСЯчейкой=Document.DeclaredItems.FindByFirstCellIdWithCommon(FirstStorage.Id)
```

### `Document.DeclaredItems.FindByProductId`
**Примеры из базы:**
```csharp
SelectedItem = select first (*) from Document.DeclaredItems.FindByProductId(SelectedProduct.ProductId) where Item.ШК==SelectedProduct.ШК
```

### `Document.DeclaredItems.Rotate`
**Примеры из базы:**
```csharp
Строки = Document.DeclaredItems.Rotate()
```

### `Document.DeclaredItems.UnderloadedOrOverloaded`
**Примеры из базы:**
```csharp
естьРасхожденияКолВа = Document.DeclaredItems.UnderloadedOrOverloaded
```

### `Document.DocumentType.Columns.Contains`
**Примеры из базы:**
```csharp
ЭтоУпаковочныйЛист = (pal != null && pal.ЭтоУпаковочныйЛист == true && Document.DocumentType.Columns.Contains("ШтрихкодУпаковочногоЛиста") == true)...
```
```csharp
Document.DocumentType.Columns.Contains("BindingKey")
```

### `Document.DocumentType.Name`
**Примеры из базы:**
```csharp
Склад.Адресный == true && Document.CreatedOnPDA && GlobalVars.РежимЯчейки[Document.DocumentType.Name] == false
```
```csharp
GlobalVars.РежимРаботыПоЯчейкам[Document.DocumentType.Name] = "перед товаром"; GlobalVars.РежимЯчейки[Document.DocumentType.Name] = true;
```
```csharp
Склад.Адресный == false && Document.CreatedOnPDA && GlobalVars.РежимЯчейки[Document.DocumentType.Name] == true
```
```csharp
GlobalVars.РежимРаботыПоЯчейкам[Document.DocumentType.Name] = "без ячеек"; GlobalVars.РежимЯчейки[Document.DocumentType.Name] = false;
```
```csharp
GlobalVars.МестоПоискаСодержимого[ Document.DocumentType.Name] = "остатки"
```

### `Document.DocumentTypeName`
**Примеры из базы:**
```csharp
GlobalVars.ИдСкладаПоУмолчанию["LastChanged"] = Склад.Ид; GlobalVars.ИдСкладаПоУмолчанию[Document.DocumentTypeName] = Склад.Ид; GlobalVars.СкладПоУ...
```
```csharp
GlobalVars.ИдСкладаПоУмолчанию["LastChanged"] = СкладОткуда.Ид; GlobalVars.ИдСкладаПоУмолчанию[Document.DocumentTypeName] = СкладОткуда.Ид; GlobalV...
```
```csharp
Document.Зона=SecondStorage.Id; GlobalVars.ИдЗоныПоУмолчанию["LastChanged"] = SecondStorage.Id; GlobalVars.ИдЗоныПоУмолчанию[Document.DocumentTypeN...
```
```csharp
Document.Зона = "" GlobalVars.ИдЗоныПоУмолчанию["LastChanged"] = "" GlobalVars.ИдЗоныПоУмолчанию[Document.DocumentTypeName] = "" GlobalVars.Мод = G...
```
```csharp
Document.DocumentTypeName == "ПеремещениеПоЯчейкам" && GlobalVars.СПалетами == "ТолькоПалеты"
```

### `Document.ExpiredDate`
**Примеры из базы:**
```csharp
if (РежимРаботыСрокаГодности.Contains("производства") && SelectedProduct.RegistrationDate != null) Document.RegistrationDate = SelectedProduct.Regi...
```
```csharp
if (РежимРаботыСрокаГодности.Contains("производства")) {SelectedProduct.RegistrationDate != null ? RegistrationDate = SelectedProduct.RegistrationD...
```
```csharp
Document.RegistrationDate = RegistrationDate; Document.ExpiredDate = ExpiredDate;
```

### `Document.Id`
**Примеры из базы:**
```csharp
ReserveLine = select first (*) from Reserve where Item.ИдДокумента == Document.Id && Item.ИдСклада == WarehouseId && Item.ИдТовара == SelectedProdu...
```
```csharp
text = "Документ "+ Document.Name + " (" + Document.Id + ") обработан."; GO.WriteInformation(text);
```

### `Document.LastSelectedProduct.Clone`
**Примеры из базы:**
```csharp
SelectedProduct = Document.LastSelectedProduct.Clone()
```

### `Document.Modified`
**Примеры из базы:**
```csharp
Document.Modified = true;
```

### `Document.Name`
**Примеры из базы:**
```csharp
text = "Документ "+ Document.Name + " (" + Document.Id + ") обработан."; GO.WriteInformation(text);
```

### `Document.RegistrationDate`
**Примеры из базы:**
```csharp
if (РежимРаботыСрокаГодности.Contains("производства") && SelectedProduct.RegistrationDate != null) Document.RegistrationDate = SelectedProduct.Regi...
```
```csharp
if (РежимРаботыСрокаГодности.Contains("производства")) {SelectedProduct.RegistrationDate != null ? RegistrationDate = SelectedProduct.RegistrationD...
```
```csharp
Document.RegistrationDate = RegistrationDate; Document.ExpiredDate = ExpiredDate;
```

### `Document.ServerHosted`
**Примеры из базы:**
```csharp
Document.ServerHosted
```
```csharp
Document.ServerHosted == false && CurrentItems.Count == 1 && CurrentItems[0].МаркаИСМП == ""
```
```csharp
Document.ServerHosted == true && CurrentItem.ИдПользователя != CurrentUser.Id
```
```csharp
if (Document.ServerHosted) CurrentItem = select first (*) from Document.CurrentItems where Item.Uid == CurrentItem.Uid; DeclaredItem = CurrentItem....
```
```csharp
Document.ServerHosted == true
```

### `Document.UnderloadedOrOverloaded`
**Примеры из базы:**
```csharp
Document.UnderloadedOrOverloaded
```

## 4. Строки (SelectedLine / CurrentLine)

### `SelectedLine.BindedLine`
**Примеры из базы:**
```csharp
SelectedLine.BindedLine != null
```
```csharp
if (SelectedLine.BindedLine.ДокументОснования != "") SelectedLine.ДокументОснования = SelectedLine.BindedLine.ДокументОснования if (SelectedLine.Bi...
```
```csharp
if (BindedLine == null || BindedLine.Uid != SelectedLine.BindedLineUid) BindedLine = SelectedLine.BindedLine;
```
```csharp
BindedLine = SelectedLine.BindedLine;
```
```csharp
if (SelectedLine.BindedLine.ДокументОснования != "") SelectedLine.ДокументОснования = SelectedLine.BindedLine.ДокументОснования if (SelectedLine.Bi...
```

### `SelectedLine.BindedLineUid`
**Примеры из базы:**
```csharp
СтрокаПлана = select first * from СтрокиПоказа where Item.Uid == SelectedLine.BindedLineUid
```
```csharp
if (BindedLine == null || BindedLine.Uid != SelectedLine.BindedLineUid) BindedLine = SelectedLine.BindedLine;
```

### `SelectedLine.BindingKey`
**Примеры из базы:**
```csharp
if (bindedLine == null || bindedLine.BindingKey != SelectedLine.BindingKey) bindedLine = select first (*) from Document.DeclaredItems where Item.Bi...
```
```csharp
di = select first (*) from Document.DeclaredItems where Item.BindingKey == SelectedLine.BindingKey; if (di != null && di.КодСтроки != 0) SelectedLi...
```

### `SelectedLine.Clone`
**Примеры из базы:**
```csharp
TUContains = select (*) from ТранспортныеУпаковки where Item.ШтрихкодРодителяТУ == SelectedLine.ШтрихкодТУ; if (TUContains == null || TUContains.Co...
```
```csharp
Document.ТранспортныеУпаковкиФакт.Add(SelectedLine.Clone());
```
```csharp
currentItems.Add(SelectedLine.Clone())
```

### `SelectedLine.CreatedBy`
**Примеры из базы:**
```csharp
if (SelectedLine.CreatedBy == "Unknown") SelectedLine.CreatedBy = Document.ServerHosted ? "Server" : "Device"
```
```csharp
SelectedLine.IsDeviceCreated || SelectedLine.CreatedBy.ToString() == "Server"
```
```csharp
if (Document.CreatedOnPDA || SelectedLine.BindedLine.IsDeviceCreated || SelectedLine.CreatedBy.ToString() == "Server") SelectedLine.BindedLine.SSCC...
```
```csharp
if (Document.CreatedOnPDA || SelectedLine.BindedLine.IsDeviceCreated || SelectedLine.CreatedBy.ToString() == "Server") { SelectedLine.BindedLine.Se...
```
```csharp
(SelectedLine.IsDeviceCreated || SelectedLine.CreatedBy.ToString() == "Server") || (SelectedLine.DeclaredQuantity > SelectedLine.ParentCurrentItems...
```

### `SelectedLine.CurrentQuantity`
**Примеры из базы:**
```csharp
SelectedLine.CurrentQuantity+SelectedProduct.Quantity>SelectedLine.DeclaredQuantity
```
```csharp
if (LastChangedCurrentItems.Count != 0 && LastChangedCurrentItems[0].DeclaredQuantity == 0) LastChangedCurrentItems[0].DeclaredQuantity = SelectedL...
```
```csharp
SelectedLine.CurrentQuantity + SelectedProduct.Quantity > SelectedLine.DeclaredQuantity
```
```csharp
SelectedLine.CurrentQuantity = SelectedLine.CurrentQuantity + SelectedProduct.Quantity;
```
```csharp
if (SelectedLine.DeclaredQuantity == 0) SelectedLine.DeclaredQuantity = SelectedLine.CurrentQuantity;
```

### `SelectedLine.CurrentQuantityWithBinding`
**Примеры из базы:**
```csharp
SelectedLine.CurrentQuantityWithBinding = SelectedLine.DeclaredQuantity
```

### `SelectedLine.DeclaredQuantity`
**Примеры из базы:**
```csharp
SelectedLine.CurrentQuantityWithBinding = SelectedLine.DeclaredQuantity
```
```csharp
mc = select (*) from SelectedLine.ParentCurrentItems where Item.МаркаИСМП != "" && Item.IsDeviceCreated == false && Item.CreatedBy.ToString() != "S...
```
```csharp
SelectedLine.CurrentQuantity+SelectedProduct.Quantity>SelectedLine.DeclaredQuantity
```
```csharp
if (LastChangedCurrentItems.Count != 0 && LastChangedCurrentItems[0].DeclaredQuantity == 0) LastChangedCurrentItems[0].DeclaredQuantity = SelectedL...
```
```csharp
SelectedLine.CurrentQuantity + SelectedProduct.Quantity > SelectedLine.DeclaredQuantity
```

### `SelectedLine.DocumentType`
**Примеры из базы:**
```csharp
(SelectedLine.DocumentType.Name.Contains("ЕГАИС") || SelectedLine.DocumentType.Name.Contains("Алко")) && SelectedLine.DocumentType.Name != "ГруппаА...
```
```csharp
GlobalVars.ВидимостьОпераций[SelectedLine.DocumentType.Name] = GlobalVars.ВидимостьОпераций["ГруппаАлко"]
```

### `SelectedLine.FieldName`
**Примеры из базы:**
```csharp
SelectedProduct.Fields.Add(SelectedLine.FieldName, SelectedLine.Value)
```

### `SelectedLine.FirstStorageId`
**Примеры из базы:**
```csharp
if (BindedLine.ДокументОснования != "") SelectedLine.ДокументОснования = BindedLine.ДокументОснования; if (BindedLine.Назначение != "") SelectedLin...
```
```csharp
SelectedLine.FirstStorageId = SelectedProduct.FirstStorageId; SelectedProduct.SSCC != "" ? SelectedLine.SSCC = SelectedProduct.SSCC : null; Selecte...
```
```csharp
SelectedLine.FirstStorageId = FirstStorage.Id
```

### `SelectedLine.IsDeviceCreated`
**Примеры из базы:**
```csharp
SelectedLine.IsDeviceCreated
```
```csharp
SelectedLine.IsDeviceCreated || SelectedLine.CreatedBy.ToString() == "Server"
```
```csharp
(SelectedLine.IsDeviceCreated || SelectedLine.CreatedBy.ToString() == "Server") || (SelectedLine.DeclaredQuantity > SelectedLine.ParentCurrentItems...
```

### `SelectedLine.Name`
**Примеры из базы:**
```csharp
row = new Cleverence.Warehouse.Row(); row.ProductId = SelectedLine.ProductId; row.ProductName = SelectedLine.Name; row.ИННДокумента = Document.ИННВ...
```

### `SelectedLine.Packing`
**Примеры из базы:**
```csharp
ПланСтроки = SelectedProduct.Product.BasePacking.ConvertFrom(SelectedLine.DeclaredQuantity,SelectedLine.Packing); ФактСтроки = SelectedProduct.Prod...
```
```csharp
SelectedProduct.Quantity = SelectedLine.Packing.ConvertFrom(ОсталосьЗаполнить,SelectedProduct.Product.BasePacking); ДобавитьВФакт = ДобавитьВФакт -...
```
```csharp
SelectedProduct.Quantity = SelectedLine.Packing.ConvertFrom(ДобавитьВФакт,SelectedProduct.Product.BasePacking) ВсегоОсталосьЗаполнить = ВсегоОстало...
```
```csharp
tempLine = new Cleverence.Warehouse.Row(); tempLine.Barcode = SelectedLine.Product.Barcode; tempLine.PackingName = SelectedLine.Packing.Name; tempL...
```

### `SelectedLine.PackingId`
**Примеры из базы:**
```csharp
if (SelectedLine.ProductId == UnknownProduct.Id && SelectedLine.ProductId != SelectedProduct.ProductId) { SelectedLine.ProductId = SelectedProduct....
```
```csharp
SelectedLine.ProductId = SelectedProduct.ProductId; SelectedLine.PackingId = SelectedProduct.PackingId; SelectedLine.ИдЕдиницыИзмерения = SelectedP...
```
```csharp
SelectedProduct = SelectedLine.Product.Pack(SelectedLine.PackingId, 1); SelectedProduct.Quantity = SelectedLine.DeclaredQuantity - SelectedLine.Cur...
```
```csharp
SelectedProduct = SelectedLine.Product.Pack(SelectedLine.PackingId, 1); SelectedProduct.Quantity = SelectedLine.DeclaredQuantity; SelectedProduct.М...
```

### `SelectedLine.ParentCurrentItems`
**Примеры из базы:**
```csharp
mc = select (*) from SelectedLine.ParentCurrentItems where Item.МаркаИСМП != "" && Item.IsDeviceCreated == false && Item.CreatedBy.ToString() != "S...
```
```csharp
CurrentItems = SelectedLine.ParentCurrentItems;
```
```csharp
CurrentItems = SelectedLine.ParentCurrentItems; DocumentLines.Remove(SelectedLine);
```
```csharp
SelectedLine.КоличествоМест = SelectedLine.ParentCurrentItems.Count
```
```csharp
CurrentItems.AddRange(SelectedLine.ParentCurrentItems)
```

### `SelectedLine.Product`
**Примеры из базы:**
```csharp
SelectedProduct = SelectedLine.Product.Pack(SelectedLine.PackingId, 1); SelectedProduct.Quantity = SelectedLine.DeclaredQuantity - SelectedLine.Cur...
```
```csharp
SelectedProduct = SelectedLine.Product.Pack(SelectedLine.PackingId, 1); SelectedProduct.Quantity = SelectedLine.DeclaredQuantity; SelectedProduct.М...
```
```csharp
{SelectedLine.Product.withsn==1}
```
```csharp
СтрокиДляПравки.Count == 1 && SelectedLine.Product.withsn != 1
```
```csharp
SelectedLine.Product.withsn == 1&&Document.докРежимСН != "Выкл"
```

### `SelectedLine.ProductId`
**Примеры из базы:**
```csharp
SelectedLine.ProductId == SelectedProduct.ProductId && SelectedLine.ИдХарактеристики == SelectedProduct.ИдХарактеристики
```
```csharp
if (SelectedLine.ProductId == UnknownProduct.Id && SelectedLine.ProductId != SelectedProduct.ProductId) { SelectedLine.ProductId = SelectedProduct....
```
```csharp
SelectedLine.Марка != "" && SelectedLine.ProductId == UnknownProduct.Id && SelectedLine.ProductId != SelectedProduct.ProductId
```
```csharp
SelectedLine.ProductId = SelectedProduct.ProductId; SelectedLine.PackingId = SelectedProduct.PackingId; SelectedLine.ИдЕдиницыИзмерения = SelectedP...
```
```csharp
row = new Cleverence.Warehouse.Row(); row.ProductId = SelectedLine.ProductId; row.ProductName = SelectedLine.Name; row.ИННДокумента = Document.ИННВ...
```

### `SelectedLine.SSCC`
**Примеры из базы:**
```csharp
if(SelectedLine.SSCC != "") SelectedLine.SSCC = "";
```
```csharp
if (BindedLine.ДокументОснования != "") SelectedLine.ДокументОснования = BindedLine.ДокументОснования; if (BindedLine.Назначение != "") SelectedLin...
```
```csharp
(SelectedLine.SSCC == "" || SelectedProduct.SSCC == "" || SelectedLine.SSCC == SelectedProduct.SSCC || SelectedLine.ДобавленаТУ > 1)
```
```csharp
if (Document.CreatedOnPDA == false) { SelectedLine.SSCC = ""; SelectedLine.ГрупповаяУпаковка = ""; SelectedLine.ШтрихкодРодителяТУ = ""; }
```
```csharp
if (Document.CreatedOnPDA == false) { SelectedLine.SSCC = ""; SelectedLine.ИдКоробки = ""; SelectedLine.ШтрихкодРодителя = ""; SelectedLine.ИдРодит...
```

### `SelectedLine.SecondStorageBarcode`
**Примеры из базы:**
```csharp
SelectedLine.SecondStorageId=SecondStorage.Id; SelectedLine.SecondStorageBarcode=SecondStorage.Barcode;
```

### `SelectedLine.SecondStorageId`
**Примеры из базы:**
```csharp
if (BindedLine.ДокументОснования != "") SelectedLine.ДокументОснования = BindedLine.ДокументОснования; if (BindedLine.Назначение != "") SelectedLin...
```
```csharp
SelectedLine.SecondStorageId=SecondStorage.Id; SelectedLine.SecondStorageBarcode=SecondStorage.Barcode;
```

### `SelectedLine.SourceAI`
**Примеры из базы:**
```csharp
Entries.Add(SelectedLine.SourceAI, SelectedLine.SourceValue);
```

### `SelectedLine.SourceValue`
**Примеры из базы:**
```csharp
Entries.Add(SelectedLine.SourceAI, SelectedLine.SourceValue);
```

### `SelectedLine.Underload`
**Примеры из базы:**
```csharp
Document.КонтрольКолва == 1 && (qty-oldqty) > SelectedLine.Underload
```

### `SelectedLine.UnderloadedOrOverloaded`
**Примеры из базы:**
```csharp
if (SelectedLine.UnderloadedOrOverloaded == true) DocumentLines.TopBottom(SelectedLine, true); else DocumentLines.Remove(SelectedLine);
```
```csharp
SelectedLine.UnderloadedOrOverloaded == true
```
```csharp
УдалятьСходящиеся && SelectedLine.UnderloadedOrOverloaded == false
```
```csharp
SelectedLine.UnderloadedOrOverloaded == false
```
```csharp
СтрокиПоказа = СтрокиПодбора; СтрокиДляСпускаВниз = СтрокиТекущегоТовара; УдалятьСходящиеся = РасхожденияЛи; СтрокаДляСпуска = select first (*) fro...
```

### `SelectedLine.Value`
**Примеры из базы:**
```csharp
SelectedProduct.Fields.Add(SelectedLine.FieldName, SelectedLine.Value)
```

## 6. Cleverence API (Специфичные классы)

### `Cleverence.Barcoding.Ean128.AutoFormatEnabled`
**Примеры из базы:**
```csharp
global::Cleverence.Barcoding.Ean128.AutoFormatEnabled = true;
```
```csharp
ScannedBarcode.Length >= 24 && global::Cleverence.Barcoding.Ean128.AutoFormatEnabled
```
```csharp
temp = global::Cleverence.Barcoding.Ean128.AutoFormatEnabled; global::Cleverence.Barcoding.Ean128.AutoFormatEnabled = true;
```
```csharp
global::Cleverence.Barcoding.Ean128.AutoFormatEnabled = temp
```

### `Cleverence.Barcoding.Ean128.FormatAnyway`
**Примеры из базы:**
```csharp
temp = global::Cleverence.Barcoding.Ean128.FormatAnyway(ScannedBarcode); ScannedBarcode = temp != empty?temp:ScannedBarcode; Коды = global::Clevere...
```

### `Cleverence.MOTP.Utils.GetMRP`
**Примеры из базы:**
```csharp
encoded = BarcodeData.ScannedBarcodeCompatible.Substring(21, 4); PricePerUnit = global::Cleverence.MOTP.Utils.GetMRP(encoded);
```

### `Cleverence.Warehouse.Compact.AdvancedOps.FindCell`
**Примеры из базы:**
```csharp
Ячейка = global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell(ПолеПоиска); CellName = Ячейка;
```
```csharp
if (FirstStorage == null && СтрокиОстатков[0].ИдЯчейки != "") FirstStorage = global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell(СтрокиОстатк...
```
```csharp
Ячейка = global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell(BarcodeData.BarcodeRaw); ЭтоЯчейка = Ячейка != null;
```

### `Cleverence.Warehouse.Compact.AdvancedOps.FindPallet`
**Примеры из базы:**
```csharp
if (BarcodeData != null) { if (BarcodeData.IsGS1Compatible) Barcode = BarcodeData.BarcodeGS1Formatted; else Barcode = BarcodeData.BarcodeRaw; Транс...
```
```csharp
temp = global::Cleverence.Barcoding.Ean128.FormatAnyway(ScannedBarcode); ScannedBarcode = temp != empty?temp:ScannedBarcode; Коды = global::Clevere...
```
```csharp
ТУ = global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet(BarcodeData.BarcodeRaw); if (ТУ != null && ТУ.ЭтоБлок == false) ТУ == null;
```
```csharp
pal = global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet(bd.BarcodeRaw);
```
```csharp
SSCCPallet = global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet(bd.BarcodeRaw);
```

### `Cleverence.Warehouse.Compact.AdvancedOps.PackProduct`
**Примеры из базы:**
```csharp
SelectedProduct = global::Cleverence.Warehouse.Compact.AdvancedOps.PackProduct(СтрокаКМОстатки.ИдТовара, СтрокаКМОстатки.ИдЕдиницыИзмерения)
```
```csharp
if (ВыборПоМарке.ИдТовара != "" && ВыборПоМарке.ИдЕдиницыИзмерения != "") SelectedProduct = global::Cleverence.Warehouse.Compact.AdvancedOps.PackPr...
```

### `Cleverence.Warehouse.DeviceInfo.GeneralFields`
**Примеры из базы:**
```csharp
global::Cleverence.Warehouse.DeviceInfo.GeneralFields["ИдУзла"] = ""
```
```csharp
GlobalVars.ИдУзла = ДоступныеУзлы[0].Ид; global::Cleverence.Warehouse.DeviceInfo.GeneralFields["ИдУзла"] = ДоступныеУзлы[0].Ид;
```
```csharp
GlobalVars.ИдУзла = SelectedItem == null ? "" : SelectedItem.Ид; global::Cleverence.Warehouse.DeviceInfo.GeneralFields["ИдУзла"] = GlobalVars.ИдУзла;
```
```csharp
global::Cleverence.Warehouse.DeviceInfo.GeneralFields["ИдУзла"] = GlobalVars.ИдУзла
```

### `Cleverence.Warehouse.DocumentItemCollection`
**Примеры из базы:**
```csharp
DocumentLines = new Cleverence.Warehouse.DocumentItemCollection(); DocumentLines.AddRange((select (*) from DeclaredItems where Item.CurrentQuantity...
```
```csharp
DeclaredItems = new Cleverence.Warehouse.DocumentItemCollection(); CheckPallet = CurrentItem.SSCC == SelectedProduct.SSCC || CurrentItem.SSCC == ""...
```
```csharp
DocumentLines = new Cleverence.Warehouse.DocumentItemCollection();
```
```csharp
ds_СписокДляВыбора = new Cleverence.Warehouse.DocumentItemCollection();
```
```csharp
if (СтрокиТекущегоТовара == null) СтрокиТекущегоТовара = new Cleverence.Warehouse.DocumentItemCollection()
```

### `Cleverence.Warehouse.DocumentTable`
**Примеры из базы:**
```csharp
СтрокаТУ.ParentTable == "Cleverence.Warehouse.DocumentTable"
```

### `Cleverence.Warehouse.DocumentType`
**Примеры из базы:**
```csharp
АлкоОперации = new Cleverence.Warehouse.DocumentType()
```

### `Cleverence.Warehouse.HybridCollection`
**Примеры из базы:**
```csharp
Сумма = new Cleverence.Warehouse.HybridCollection()
```
```csharp
СтрокиПоказа = new Cleverence.Warehouse.HybridCollection()
```

### `Cleverence.Warehouse.ObjectCollection`
**Примеры из базы:**
```csharp
скидки = new Cleverence.Warehouse.ObjectCollection()
```
```csharp
Buffer = new Cleverence.Warehouse.ObjectCollection()
```
```csharp
Buffer = new Cleverence.Warehouse.ObjectCollection(); ПоискВОстатках = new Cleverence.Warehouse.RowCollection(); НайденныеТовары = new Cleverence.W...
```

### `Cleverence.Warehouse.PackedProduct`
**Примеры из базы:**
```csharp
SelectedProduct = new Cleverence.Warehouse.PackedProduct(ProductLine.ProductId, ProductLine.PackingId); if (SelectedProduct.Product == null || Sele...
```
```csharp
if (SelectedLine.ИдТовара != "" && SelectedLine.ИдЕдиницыИзмерения != "") SelectedProduct = new Cleverence.Warehouse.PackedProduct(SelectedLine.ИдТ...
```
```csharp
SelectedProduct = new Cleverence.Warehouse.PackedProduct(SelectedLine.ИдТовара, SelectedLine.ИдЕдиницыИзмерения);
```
```csharp
УпаковкаДляКонвертации = new Cleverence.Warehouse.PackedProduct(SelectedLine.ИдТовара, SelectedLine.ИдЕдиницыИзмерения).Packing
```
```csharp
СтрокаКМ = СтрокаКМОстатки; SelectedProduct = new Cleverence.Warehouse.PackedProduct(СтрокаКМ.ИдТовара, СтрокаКМ.ИдЕдиницыИзмерения); if (SelectedP...
```

### `Cleverence.Warehouse.PackedProductCollection`
**Примеры из базы:**
```csharp
PackedProductsList = new Cleverence.Warehouse.PackedProductCollection()
```

### `Cleverence.Warehouse.ProductsManager.AddToCache`
**Примеры из базы:**
```csharp
global::Cleverence.Warehouse.ProductsManager.AddToCache(SelectedProduct)
```

### `Cleverence.Warehouse.ProductsManager.FindById`
**Примеры из базы:**
```csharp
ТоварОтбор = global::Cleverence.Warehouse.ProductsManager.FindById(SelectedLine.ИдТовара)
```

### `Cleverence.Warehouse.ProductsManager.FindPackingById`
**Примеры из базы:**
```csharp
УпакОтбор = global::Cleverence.Warehouse.ProductsManager.FindPackingById(SelectedLine.ИдТовара, SelectedLine.ИдЕдиницыИзмерения)
```

### `Cleverence.Warehouse.Row`
**Примеры из базы:**
```csharp
Строка = new Cleverence.Warehouse.Row()
```
```csharp
ТекущаяКоробка = new Cleverence.Warehouse.Row(); ТекущаяКоробка.Ид = BarcodeData.ScannedBarcodeCompatible; ТекущаяКоробка.Родитель = ""; ТекущаяКор...
```
```csharp
ТекущаяПалета = new Cleverence.Warehouse.Row(); ТекущаяПалета.Ид = ТранспортнаяУпаковка != "" ? ТранспортнаяУпаковка.Barcode : ScannedBarcode; Теку...
```
```csharp
ПоискКоробки = new Cleverence.Warehouse.Row(); ПоискКоробки.Ид = BarcodeData.ScannedBarcodeCompatible; ПоискКоробки.Статус = "Закрыта"; ПоискКоробк...
```
```csharp
ПоискПалеты = new Cleverence.Warehouse.Row(); ПоискПалеты.Ид = ТранспортнаяУпаковка.Barcode; ПоискПалета.Родитель == ""; ПоискПалеты.СерийныйНомер ...
```

### `Cleverence.Warehouse.RowCollection`
**Примеры из базы:**
```csharp
Строки = new Cleverence.Warehouse.RowCollection()
```
```csharp
НетДанных = true; СтрокиТУ = new Cleverence.Warehouse.RowCollection(); СтрокиОстатков = new Cleverence.Warehouse.RowCollection(); СтрокаТУ = Трансп...
```
```csharp
Buffer = new Cleverence.Warehouse.ObjectCollection(); ПоискВОстатках = new Cleverence.Warehouse.RowCollection(); НайденныеТовары = new Cleverence.W...
```
```csharp
ОтображаемаяКоллекция = new Cleverence.Warehouse.RowCollection(); ОтображаемаяКоллекция.AddRange(ОтображаемыеСтроки);
```
```csharp
Result = new Cleverence.Warehouse.RowCollection(); Result.Add(info);
```

### `Cleverence.Warehouse.StringCollection`
**Примеры из базы:**
```csharp
stringBarcode = "(01)" + BarcodeData.GTIN infoFields = new Cleverence.Warehouse.StringCollection() infoFields.Add("(01) " + BarcodeData.GTIN) if (U...
```

## 7. Общие методы (Коллекции, Строки, Даты)

### `AdvancedOps.FindCell`
**Примеры из базы:**
```csharp
Ячейка = global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell(ПолеПоиска); CellName = Ячейка;
```
```csharp
if (FirstStorage == null && СтрокиОстатков[0].ИдЯчейки != "") FirstStorage = global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell(СтрокиОстатк...
```
```csharp
Ячейка = global::Cleverence.Warehouse.Compact.AdvancedOps.FindCell(BarcodeData.BarcodeRaw); ЭтоЯчейка = Ячейка != null;
```

### `AdvancedOps.FindPallet`
**Примеры из базы:**
```csharp
if (BarcodeData != null) { if (BarcodeData.IsGS1Compatible) Barcode = BarcodeData.BarcodeGS1Formatted; else Barcode = BarcodeData.BarcodeRaw; Транс...
```
```csharp
temp = global::Cleverence.Barcoding.Ean128.FormatAnyway(ScannedBarcode); ScannedBarcode = temp != empty?temp:ScannedBarcode; Коды = global::Clevere...
```
```csharp
ТУ = global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet(BarcodeData.BarcodeRaw); if (ТУ != null && ТУ.ЭтоБлок == false) ТУ == null;
```
```csharp
pal = global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet(bd.BarcodeRaw);
```
```csharp
SSCCPallet = global::Cleverence.Warehouse.Compact.AdvancedOps.FindPallet(bd.BarcodeRaw);
```

### `AdvancedOps.PackProduct`
**Примеры из базы:**
```csharp
SelectedProduct = global::Cleverence.Warehouse.Compact.AdvancedOps.PackProduct(СтрокаКМОстатки.ИдТовара, СтрокаКМОстатки.ИдЕдиницыИзмерения)
```
```csharp
if (ВыборПоМарке.ИдТовара != "" && ВыборПоМарке.ИдЕдиницыИзмерения != "") SelectedProduct = global::Cleverence.Warehouse.Compact.AdvancedOps.PackPr...
```

### `BadBarcode.Replace`
**Примеры из базы:**
```csharp
BadBarcode = BadBarcode.Replace(GS, "<b><blue>GS</blue></b>"); BadBarcode = BadBarcode.Replace(FNC1, "<b><blue>FNC1</blue></b>"); BadBarcode = BadB...
```

### `Barcode.Replace`
**Примеры из базы:**
```csharp
Разделитель = Barcode.Substring(31, 1); if (global::System.Char.IsControl(Barcode, 31) || Разделитель == FNC1) КМ = Barcode.Replace(Разделитель, "");
```
```csharp
Разделитель = Barcode.Substring(25, 1); if (global::System.Char.IsControl(Barcode, 25) || Разделитель == FNC1) КМ = Barcode.Replace(Разделитель, "");
```
```csharp
GoodBarcode = Barcode.Replace("<", "\\<")
```

### `Barcode.StartsWith`
**Примеры из базы:**
```csharp
Barcode.StartsWith("(") != true
```

### `Barcode.Substring`
**Примеры из базы:**
```csharp
if (ЭтоБлок == true) строкиНаУдаление = select (*) from Document.CurrentItems where Item.ГрупповаяУпаковка == Barcode || Item.ГрупповаяУпаковка == ...
```
```csharp
КМ = Barcode.Substring(0, 24) + GS + Barcode.Substring(24)
```
```csharp
КМ = Barcode.Substring(0, 31) + GS + Barcode.Substring(31)
```
```csharp
КМ = Barcode.Substring(0, 31) + GS + Barcode.Substring(31, 14) + GS + Barcode.Substring(45)
```
```csharp
Разделитель = Barcode.Substring(31, 1); if (global::System.Char.IsControl(Barcode, 31) || Разделитель == FNC1) КМ = Barcode.Replace(Разделитель, "");
```

### `BarcodeCleared.Replace`
**Примеры из базы:**
```csharp
if (BarcodeData.IsGS1Compatible) Barcode = BarcodeData.BarcodeGS1Cleared; else Barcode = BarcodeData.BarcodeCleared.Replace(" ","").Replace(FNC1, "...
```

### `BarcodeRaw.StartsWith`
**Примеры из базы:**
```csharp
ЭтоКМ == false && (BarcodeData.IsMark == false || BarcodeData.BarcodeRaw.StartsWith("è") == true) && ВосстанавливатьКМ
```
```csharp
bd = BarcodeData.IsGS1Compatible && BarcodeData.BarcodeRaw.Length != 26 && BarcodeData.BarcodeRaw.StartsWith("3465") == false ? GO.GetBarcodeData(B...
```
```csharp
BarcodeData.IsMark == false || BarcodeData.BarcodeRaw.StartsWith("è") == true
```

### `BarcodeRaw.Substring`
**Примеры из базы:**
```csharp
(BarcodeData.IsTobaccoPack || (BarcodeData.BarcodeRaw.Length == 25 || BarcodeData.BarcodeRaw.Length == 21) && GO.GetBarcodeData(BarcodeData.Barcode...
```
```csharp
GO.GetBarcodeData(BarcodeData.BarcodeRaw.Substring(0, 14)).IsGTINCompatible
```
```csharp
GTIN = BarcodeData.BarcodeRaw.Substring(0, 14)
```
```csharp
IdentificationCode = BarcodeData.BarcodeRaw.Substring(0, 21)
```
```csharp
GTIN = GO.GetBarcodeData(BarcodeData.BarcodeRaw.Substring(0,14))
```

### `BasePacking.ConvertFrom`
**Примеры из базы:**
```csharp
SelectedProduct.Quantity = SelectedProduct.Product.BasePacking.ConvertFrom(SelectedProduct.Quantity,SelectedProduct.Packing); SelectedProduct.Цена ...
```
```csharp
ДопустимыйПеревес = 1; ДопустимыйПеревес = ДопустимыйПеревес + (GlobalVars.КоэффициентПревышенияМеры != 0.0 ? GlobalVars.КоэффициентПревышенияМеры ...
```
```csharp
ПланСтроки = SelectedProduct.Product.BasePacking.ConvertFrom(SelectedLine.DeclaredQuantity,SelectedLine.Packing); ФактСтроки = SelectedProduct.Prod...
```
```csharp
КоличествоПлан = СтрокиТекущегоТовара.DeclaredQuantity; КоличествоФакт = СтрокиТекущегоТовара.CurrentQuantity; ВсегоОсталосьЗаполнить = КоличествоП...
```

### `Buffer.Add`
**Примеры из базы:**
```csharp
Buffer.Add(SelectedProduct)
```

### `Char.IsControl`
**Примеры из базы:**
```csharp
Разделитель = Barcode.Substring(31, 1); if (global::System.Char.IsControl(Barcode, 31) || Разделитель == FNC1) КМ = Barcode.Replace(Разделитель, "");
```
```csharp
Разделитель = Barcode.Substring(25, 1); if (global::System.Char.IsControl(Barcode, 25) || Разделитель == FNC1) КМ = Barcode.Replace(Разделитель, "");
```

### `Char.IsDigit`
**Примеры из базы:**
```csharp
while (idx < sub1.Length) { if (global::System.Char.IsDigit(sub1, idx) == false) hasChar = true; idx = idx + 1; }
```

### `CheckMark.GetAlcoCode`
**Примеры из базы:**
```csharp
AlcoCode = CheckMark.GetAlcoCode(BarcodeData.BarcodeRaw)
```
```csharp
SelectedProduct.Марка = ScannedBarcode; SelectedProduct.МаркаИСМП = ScannedBarcode; if(ScannedBarcode.Length == 68) SelectedProduct.АлкоКод = Check...
```
```csharp
АлкоКод = CheckMark.GetAlcoCode(SelectedProduct.АлкоПДФ)
```

### `ClearedMC.Replace`
**Примеры из базы:**
```csharp
ClearedMC = BarcodeData.IsGS1Compatible ? BarcodeData.BarcodeGS1Cleared : BarcodeData.BarcodeCleared; ClearedMC = ClearedMC.Replace(" ","").Replace...
```

### `ClearedMC.StartsWith`
**Примеры из базы:**
```csharp
ClearedMC.StartsWith("(") == false
```

### `ClearedMC.Substring`
**Примеры из базы:**
```csharp
Length = ClearedMC.Length; if (Length == 32 || Length == 39 || Length == 40 || Length == 45 || Length == 51) AlgorythmType = "Dairy"; else if (Leng...
```
```csharp
sub1 = ClearedMC.Substring(25, 14); sub2 = ClearedMC.Substring(31, 8);
```
```csharp
if (hasChar == true && sub2.StartsWith("17")) MarkingCode = ClearedMC.Substring(0, 31) + GS + ClearedMC.Substring(31); else if (sub1.StartsWith("70...
```
```csharp
if (Length == 32) MarkingCode = ClearedMC.Substring(0, 26) + GS + ClearedMC.Substring(26); else if (Length == 39) MarkingCode = ClearedMC.Substring...
```
```csharp
if (Length == 31 || Length == 35) MarkingCode = ClearedMC.Substring(0, 25) + GS + ClearedMC.Substring(25); else if (Length == 41) MarkingCode = Cle...
```

### `Columns.Contains`
**Примеры из базы:**
```csharp
ЭтоУпаковочныйЛист = (pal != null && pal.ЭтоУпаковочныйЛист == true && Document.DocumentType.Columns.Contains("ШтрихкодУпаковочногоЛиста") == true)...
```
```csharp
Document.DocumentType.Columns.Contains("BindingKey")
```

### `Convert.ToChar`
**Примеры из базы:**
```csharp
GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString(); ДатаСкана = CurrentDate;
```
```csharp
GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString();
```
```csharp
SavedBarcode = Barcode; GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString(); BarcodeData = GO.G...
```
```csharp
GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString(); Иероглиф = global::System.Convert.ToChar(3...
```
```csharp
GS = global::System.Convert.ToChar(29).ToString(); FNC1 = global::System.Convert.ToChar(232).ToString(); NewLine = global::System.Environment.NewLi...
```

### `CreatedBy.ToString`
**Примеры из базы:**
```csharp
CurrentItem.IsDeviceCreated || CurrentItem.CreatedBy.ToString() == "Server"
```
```csharp
СтрокиПоказа != null && DeclaredItem != null && (DeclaredItem.IsDeviceCreated || DeclaredItem.CreatedBy.ToString() == "Server") && DeclaredItem.Cur...
```
```csharp
temp = select (*) from DeclaredItems where Item.IsDeviceCreated || Item.CreatedBy.ToString() == "Server"
```
```csharp
mc = select (*) from SelectedLine.ParentCurrentItems where Item.МаркаИСМП != "" && Item.IsDeviceCreated == false && Item.CreatedBy.ToString() != "S...
```
```csharp
{select (*) from LastChangedCurrentItems where Item.IsDeviceCreated == false && Item.CreatedBy.ToString() != "Server"}
```

### `CreatedItems.FindByUnderloadedOrOverloaded`
**Примеры из базы:**
```csharp
CreatedItems = select (*) from LastChangedDeclaredItems where Item.CreatedBy.ToString() == "Server"; DocumentLines.AddRange(CreatedItems.FindByUnde...
```

### `CurrentGroup.GetDocumentTypes`
**Примеры из базы:**
```csharp
СтрокиОпераций = CurrentGroup.GetDocumentTypes(false, false)
```

### `CurrentItem.Clone`
**Примеры из базы:**
```csharp
SelectedProduct = CurrentItem.Clone(); SelectedProduct.CurrentQuantity = CurrentItem.CurrentQuantity - Quantity;
```

### `CurrentItems.AddRange`
**Примеры из базы:**
```csharp
CurrentItems.AddRange(SelectedLine.ParentCurrentItems)
```
```csharp
Document.CurrentItems.Clear(); currentItems.CreatedBy = CreatedBy; Document.CurrentItems.AddRange(currentItems);
```

### `CurrentItems.Clear`
**Примеры из базы:**
```csharp
Document.CurrentItems.Clear(); currentItems.CreatedBy = CreatedBy; Document.CurrentItems.AddRange(currentItems);
```

### `CurrentPackage.Add`
**Примеры из базы:**
```csharp
CurrentPackage.Add(tmpPackage); TableItems.Add(tmpPackage);
```

### `DataItem.Contains`
**Примеры из базы:**
```csharp
if (DataItem.Contains("Цена") && DataItem.Цена > 0.0) { SelectedProduct.Цена = DataItem.Цена; } else if (SelectedProduct.Packing.Contains("Цена") &...
```

### `Decimal.Parse`
**Примеры из базы:**
```csharp
ИнтАлкоСН = global::System.Decimal.Parse(SelectedProduct.АлкоСН)
```

### `DeclaredItems.Add`
**Примеры из базы:**
```csharp
DeclaredItems.Add(CurrentItem.BindedLine);
```

### `DeclaredItems.AddRange`
**Примеры из базы:**
```csharp
Document.DeclaredItems.Clear(); Document.DeclaredItems.AddRange(declaredItems);
```

### `DeclaredItems.Clear`
**Примеры из базы:**
```csharp
Document.DeclaredItems.Clear(); Document.DeclaredItems.AddRange(declaredItems);
```

### `DeclaredItems.FindByCurrentQuantity`
**Примеры из базы:**
```csharp
DocumentLines = new Cleverence.Warehouse.DocumentItemCollection(); DocumentLines.AddRange((select (*) from DeclaredItems where Item.CurrentQuantity...
```

### `DeclaredItems.FindByFirstCellIdWithCommon`
**Примеры из базы:**
```csharp
СтрокиТовараСЯчейкой=Document.DeclaredItems.FindByFirstCellIdWithCommon(FirstStorage.Id)
```

### `DeclaredItems.FindByProductId`
**Примеры из базы:**
```csharp
SelectedItem = select first (*) from Document.DeclaredItems.FindByProductId(SelectedProduct.ProductId) where Item.ШК==SelectedProduct.ШК
```

### `DeclaredItems.FindByUnderloadedOrOverloaded`
**Примеры из базы:**
```csharp
DocumentLines = new Cleverence.Warehouse.DocumentItemCollection(); DocumentLines.AddRange((select (*) from DeclaredItems where Item.CurrentQuantity...
```
```csharp
DeclaredItems = select (*) from LastChangedDeclaredItems where Item.CreatedBy.ToString() != "Server"; DocumentLines.AddRange(CompareMode == true ? ...
```

### `DeclaredItems.Rotate`
**Примеры из базы:**
```csharp
Строки = Document.DeclaredItems.Rotate()
```

### `Document.Contains`
**Примеры из базы:**
```csharp
Document.Contains("ПриниматьЧужиеКМ") == false || Document.ПриниматьЧужиеКМ == false
```
```csharp
СессияПерваяЯчейка = FirstStorage; if (Document.Contains("СобиратьРоссыпью")) Document.СобиратьРоссыпью = false;
```
```csharp
if (Document.Contains("СобиратьРоссыпью")) Document.СобиратьРоссыпью = false; Barcode = BarcodeData.IsGS1Compatible ? BarcodeData.BarcodeGS1Formatt...
```

### `Document.ContainsField`
**Примеры из базы:**
```csharp
if (Document.ContainsField("ПоЯчейкам")) Document.ПоЯчейкам = СессияРежимЯчеек; if (Document.ContainsField("КонтрольЯчеек")) Document.КонтрольЯчеек...
```
```csharp
if (Document.ContainsField("МестоПоискаСодержимого") && Document.МестоПоискаСодержимого == "") Document.МестоПоискаСодержимого == МестоПоискаСодерж...
```
```csharp
if (Document.ContainsField("НастройкиСохранены")) Document.НастройкиСохранены = true;
```

### `DocumentLines.AddRange`
**Примеры из базы:**
```csharp
DocumentLines = new Cleverence.Warehouse.DocumentItemCollection(); DocumentLines.AddRange((select (*) from DeclaredItems where Item.CurrentQuantity...
```
```csharp
DeclaredItems = select (*) from LastChangedDeclaredItems where Item.CreatedBy.ToString() != "Server"; DocumentLines.AddRange(CompareMode == true ? ...
```
```csharp
CreatedItems = select (*) from LastChangedDeclaredItems where Item.CreatedBy.ToString() == "Server"; DocumentLines.AddRange(CreatedItems.FindByUnde...
```

### `DocumentLines.Remove`
**Примеры из базы:**
```csharp
if (SelectedLine.UnderloadedOrOverloaded == true) DocumentLines.TopBottom(SelectedLine, true); else DocumentLines.Remove(SelectedLine);
```
```csharp
DocumentLines.Remove(SelectedLine)
```
```csharp
CurrentItems = SelectedLine.ParentCurrentItems; DocumentLines.Remove(SelectedLine);
```

### `DocumentLines.TopBottom`
**Примеры из базы:**
```csharp
if (SelectedLine.UnderloadedOrOverloaded == true) DocumentLines.TopBottom(SelectedLine, true); else DocumentLines.Remove(SelectedLine);
```
```csharp
DocumentLines.TopBottom(SelectedLine, true)
```
```csharp
DocumentLines.TopBottom(SelectedLine, false)
```

### `Double.Parse`
**Примеры из базы:**
```csharp
height = global::System.Double.Parse(GlobalVars.ВысотаЭтикетки)
```
```csharp
length = global::System.Double.Parse(GlobalVars.ШиринаЭтикетки)
```

### `Ean128.FormatAnyway`
**Примеры из базы:**
```csharp
temp = global::Cleverence.Barcoding.Ean128.FormatAnyway(ScannedBarcode); ScannedBarcode = temp != empty?temp:ScannedBarcode; Коды = global::Clevere...
```

### `Entries.Add`
**Примеры из базы:**
```csharp
Entries.Add(SelectedLine.SourceAI, SelectedLine.SourceValue);
```

### `EntriesRows.Add`
**Примеры из базы:**
```csharp
Entries = NewBarcodeData.GS1.GetEntries(); ind = 0; while (ind < Entries.Length){ newRow = new Cleverence.Warehouse.Row(); newRow.AI = Entries[ind]...
```

### `ErrorMessage.Contains`
**Примеры из базы:**
```csharp
ErrorMessage.Contains("Printer connection failed") == true
```
```csharp
ErrorMessage.Contains("ошибка обработки шаблона") == true || ErrorMessage.Contains("Не удалось обработать шаблон") == true
```
```csharp
ErrorMessage.Contains("Подключение не установлено") == true
```
```csharp
ErrorMessage.Contains("Неверные параметры доступа") == true
```
```csharp
ErrorMessage.Contains("Серверу не удалось обработать запрос") == true
```

### `ExpiredDate.ToString`
**Примеры из базы:**
```csharp
stringBarcode = "(01)" + BarcodeData.GTIN infoFields = new Cleverence.Warehouse.StringCollection() infoFields.Add("(01) " + BarcodeData.GTIN) if (U...
```

### `Fields.Add`
**Примеры из базы:**
```csharp
SelectedProduct.Fields.Add(SelectedLine.FieldName, SelectedLine.Value)
```

### `Fields.Contains`
**Примеры из базы:**
```csharp
info == null || info.Fields.Contains("МаркаИСМП")
```

### `First.ToString`
**Примеры из базы:**
```csharp
SelectedProduct.sn=Prefix + First.ToString(SerialFormat)
```

### `FirstSerial.Substring`
**Примеры из базы:**
```csharp
FirstSerial.Substring(0, SerialPrefixLength) == LastSerial.Substring(0, SerialPrefixLength) == true
```
```csharp
Prefix=FirstSerial.Substring(0, SerialPrefixLength)
```
```csharp
First=global::System.Int32.Parse(FirstSerial.Substring(SerialPrefixLength))
```

### `GO.GetBarcodeData`
**Примеры из базы:**
```csharp
SelectedProduct.Штрихкод = ScannedBarcode != "0" ? ScannedBarcode : SelectedProduct.Packing.EAN13Barcode != "" ? SelectedProduct.Packing.EAN13Barco...
```
```csharp
BarcodeData = GO.GetBarcodeData("(01)00000000000000(21)TEST+TEST+123(91)TEST(92)TEST+TEST+TEST+TEST+TEST+TEST+TEST+TEST+TEST+TEST+TEST+TEST+TEST+TE...
```
```csharp
(BarcodeData.IsTobaccoPack || (BarcodeData.BarcodeRaw.Length == 25 || BarcodeData.BarcodeRaw.Length == 21) && GO.GetBarcodeData(BarcodeData.Barcode...
```
```csharp
GO.GetBarcodeData(BarcodeData.BarcodeRaw.Substring(0, 14)).IsGTINCompatible
```
```csharp
GTIN = GO.GetBarcodeData(BarcodeData.BarcodeRaw.Substring(0,14))
```

### `GO.HideWaitMessage`
**Примеры из базы:**
```csharp
GO.HideWaitMessage()
```
```csharp
GO.PlayError(); GO.HideWaitMessage();
```
```csharp
GO.HideWaitMessage(); Message = "Этикетка успешно отправлена на принтер!";
```

### `GO.Play`
**Примеры из базы:**
```csharp
GO.Play("Cell.wav")
```

### `GO.PlayError`
**Примеры из базы:**
```csharp
GO.PlayError(); ErrorMessage = "Введено неверное имя или штриход ячейки!";
```
```csharp
GO.PlayError(); ErrorMessage = "Ошибка!<br/>Отсутствует соединение с 1С! Проверьте подключение и попробуйте снова!";
```
```csharp
GO.PlayError()
```
```csharp
GO.PlayError(); ErrorMessage = "Необходимо закрыть палету!";
```
```csharp
GO.PlayError(); ErrorMessage = "Отсканирована не палета";
```

### `GO.ShowErrorBaloon`
**Примеры из базы:**
```csharp
GO.ShowErrorBaloon(ErrorMessage,2000,false)
```
```csharp
GO.ShowErrorBaloon("Количество должно быть больше 0!", 1500, true)
```

### `GO.ShowWaitMessage`
**Примеры из базы:**
```csharp
GO.ShowWaitMessage("Проверка КМ документа в ЧЗ...");
```
```csharp
GO.ShowWaitMessage("Тестовая печать..")
```
```csharp
GO.ShowWaitMessage("Идет печать..")
```

### `GO.WriteError`
**Примеры из базы:**
```csharp
GO.WriteError("Item can't be null!")
```

### `GO.WriteInformation`
**Примеры из базы:**
```csharp
text = "Документ "+ Document.Name + " (" + Document.Id + ") обработан."; GO.WriteInformation(text);
```

### `GS1.Contains`
**Примеры из базы:**
```csharp
BarcodeData.IsGS1Compatible == true && BarcodeData.GS1.Contains(01) && BarcodeData.GS1.Contains(21)
```
```csharp
BarcodeData.GS1.Contains(8005)
```
```csharp
BarcodeData.GS1.Contains("00")
```
```csharp
BarcodeData.IsGS1Compatible && (BarcodeData.GS1.Contains(01) || BarcodeData.GS1.Contains(8006))
```
```csharp
IsUniqueGS1 = BarcodeData.IsGS1Compatible == true && BarcodeData.GS1.Contains(01) && BarcodeData.GS1.Contains(21) && ((SerialNumber.Length >= 6 && ...
```

### `GS1.ContainsY`
**Примеры из базы:**
```csharp
PricePerUnit =BarcodeData.GS1.ContainsY(395) ? BarcodeData.GS1.GetDecimalValueY(395) : BarcodeData.GS1.GetDecimalValue(8005);
```

### `GS1.FillEan128ProductFields`
**Примеры из базы:**
```csharp
SelectedProduct.ШК = Barcode; SelectedProduct.ОснШК = MainBarcode != "" ? MainBarcode : SelectedProduct.Packing.MainBarcode; if (BarcodeData.IsGS1C...
```

### `GS1.GetDecimalValue`
**Примеры из базы:**
```csharp
PricePerUnit =BarcodeData.GS1.ContainsY(395) ? BarcodeData.GS1.GetDecimalValueY(395) : BarcodeData.GS1.GetDecimalValue(8005);
```

### `GS1.GetDecimalValueY`
**Примеры из базы:**
```csharp
PricePerUnit =BarcodeData.GS1.ContainsY(395) ? BarcodeData.GS1.GetDecimalValueY(395) : BarcodeData.GS1.GetDecimalValue(8005);
```
```csharp
SelectedProduct.GS1Марка = SelectedProduct.Марка; SelectedProduct.ExpiredDate = BarcodeData.GS1.Contains(17) ? BarcodeData.GS1.GetObjectValue(17) :...
```

### `GS1.GetEntries`
**Примеры из базы:**
```csharp
{BarcodeData.GS1.GetEntries()}
```
```csharp
Entries = NewBarcodeData.GS1.GetEntries(); ind = 0; while (ind < Entries.Length){ newRow = new Cleverence.Warehouse.Row(); newRow.AI = Entries[ind]...
```

### `GS1.GetObjectValue`
**Примеры из базы:**
```csharp
SelectedProduct.GS1Марка = SelectedProduct.Марка; SelectedProduct.ExpiredDate = BarcodeData.GS1.Contains(17) ? BarcodeData.GS1.GetObjectValue(17) :...
```
```csharp
if (BarcodeData.GS1.Contains("17")) ДатаСерии = BarcodeData.GS1.GetObjectValue("17"); else ДатаСерии = BarcodeData.GS1.GetObjectValue("7003");
```
```csharp
SelectedProduct.Quantity = BarcodeData.GS1.GetObjectValue(3103)
```
```csharp
ПоGS = new Cleverence.Warehouse.Row(); if (BarcodeData.GS1.Contains("10")) ПоGS.Серия = BarcodeData.GS1.GetObjectValue("10"); if (BarcodeData.GS1.C...
```

### `GS1.GetValue`
**Примеры из базы:**
```csharp
IdentificationCode = IdentificationCode + "(8005)" + BarcodeData.GS1.GetValue(8005);
```

### `GTIN.StartsWith`
**Примеры из базы:**
```csharp
BarcodeData.IsGTINCompatible && BarcodeData.GTIN.StartsWith("029") == true
```
```csharp
BarcodeData.GTIN != "" && BarcodeData.GTIN.StartsWith("02") && BarcodeData.IsGS1Compatible
```

### `GlobalVars.Contains`
**Примеры из базы:**
```csharp
GlobalVars.Contains("ОшибкаЗаписи") == false
```
```csharp
GlobalVars.Contains("СпрятатьПомощь") == false
```
```csharp
GlobalVars.Contains("СкладПоУмолчанию") == false
```
```csharp
GlobalVars.Contains("ИдСкладаПоУмолчанию") == false
```
```csharp
GlobalVars.Contains("ИдЗоныПоУмолчанию")== false
```

### `Go.GetBarcodeData`
**Примеры из базы:**
```csharp
if (SelectedProduct.Packing.EAN13Barcode != "") ScannedBarcode = SelectedProduct.Packing.EAN13Barcode; else if (SelectedProduct.Packing.GTINBarcode...
```

### `Go.PlayError`
**Примеры из базы:**
```csharp
Go.PlayError()
```

### `GoodBarcode.Replace`
**Примеры из базы:**
```csharp
GoodBarcode = GoodBarcode.Replace(GS, "<b><blue>GS</blue></b>"); GoodBarcode = GoodBarcode.Replace(FNC1, "<b><blue>FNC1</blue></b>"); GoodBarcode =...
```

### `Guid.NewGuid`
**Примеры из базы:**
```csharp
Серия.Ид = global::System.Guid.NewGuid().ToString()
```

### `Int32.Parse`
**Примеры из базы:**
```csharp
First=global::System.Int32.Parse(FirstSerial.Substring(SerialPrefixLength))
```
```csharp
Last=global::System.Int32.Parse(LastSerial.Substring(SerialPrefixLength))
```
```csharp
Contrast = global::System.Int32.Parse(GlobalVars.Contrast)
```

### `InventoryItemAttributes.Add`
**Примеры из базы:**
```csharp
Attribute = new Row(); Attribute.ИмяХарактеристики = "без характеристики"; Attribute.Ид = SelectedLine.ИдХарактеристики; InventoryItemAttributes.Ad...
```
```csharp
InventoryItemAttributes.Add(Attribute)
```
```csharp
Attribute = new Row(); Attribute.ИмяХарактеристики = "без имени"; Attribute.Ид = SelectedLine.ИдХарактеристики; InventoryItemAttributes.Add(Attribu...
```

### `InventoryItemSeries.Add`
**Примеры из базы:**
```csharp
SeriesLine = new Row(); SeriesLine.ИмяСерии = "без серии"; SeriesLine.Ид = SelectedLine.ИдСерии; InventoryItemSeries.Add(SeriesLine);
```
```csharp
InventoryItemSeries.Add(SeriesLine)
```
```csharp
SeriesLine = new Row(); SeriesLine.ИмяСерии = "без имени"; SeriesLine.Ид = SelectedLine.ИдСерии; InventoryItemSeries.Add(SeriesLine);
```

### `LastChangedDeclaredItems.Add`
**Примеры из базы:**
```csharp
LastChangedDeclaredItems = new Cleverence.Warehouse.DocumentItemCollection(); LastChangedDeclaredItems.Add(SelectedLine);
```

### `LastChangedDeclaredItems.FindByUnderloadedOrOverloaded`
**Примеры из базы:**
```csharp
{LastChangedDeclaredItems.FindByUnderloadedOrOverloaded(true)}
```

### `LastSelectedProduct.Clone`
**Примеры из базы:**
```csharp
SelectedProduct = LastSelectedProduct.Clone();
```
```csharp
SelectedProduct = Document.LastSelectedProduct.Clone()
```

### `LastSerial.Substring`
**Примеры из базы:**
```csharp
FirstSerial.Substring(0, SerialPrefixLength) == LastSerial.Substring(0, SerialPrefixLength) == true
```
```csharp
Last=global::System.Int32.Parse(LastSerial.Substring(SerialPrefixLength))
```

### `List.Add`
**Примеры из базы:**
```csharp
tempLine = new Cleverence.Warehouse.Row(); tempLine.Barcode = SelectedLine.Product.Barcode; tempLine.PackingName = SelectedLine.Packing.Name; tempL...
```

### `MathOperations.Round`
**Примеры из базы:**
```csharp
Quantity1 = MathOperations.Round(Quantity,7,0); Quantity = Quantity1 == MathOperations.Round(Quantity,0,0) ? Quantity1 : Quantity;
```

### `Name.Contains`
**Примеры из базы:**
```csharp
(SelectedLine.DocumentType.Name.Contains("ЕГАИС") || SelectedLine.DocumentType.Name.Contains("Алко")) && SelectedLine.DocumentType.Name != "ГруппаА...
```
```csharp
SelectedItem = null; PastName = СтрокаПоиска; LineByName = select (*) from Collection where Item.Product.Name.Contains(СтрокаПоиска);
```

### `OneCConnectorCheckDate.AddMinutes`
**Примеры из базы:**
```csharp
GlobalVars.OneCConnectorCheckDate != EmptyDate && GlobalVars.OneCConnectorCheckDate.AddMinutes(minutes) > CurrentDate
```

### `PackedProductsList.TopBottom`
**Примеры из базы:**
```csharp
PackedProductsList.TopBottom(SelectedProduct, true); MarkingCodeInfo = SelectedProduct.Марка != "";
```
```csharp
PackedProductsList.TopBottom(SelectedProduct, true)
```

### `Packing.Contains`
**Примеры из базы:**
```csharp
if (DataItem.Contains("Цена") && DataItem.Цена > 0.0) { SelectedProduct.Цена = DataItem.Цена; } else if (SelectedProduct.Packing.Contains("Цена") &...
```

### `Packing.ConvertFrom`
**Примеры из базы:**
```csharp
SelectedLine.ВНаличии = SelectedProduct.Packing.ConvertFrom(SelectedLine.КоличествоВНаличии,УпаковкаДляКонвертации); SelectedLine.КРазмещению = Sel...
```
```csharp
SelectedProduct.Quantity = SelectedLine.Packing.ConvertFrom(ОсталосьЗаполнить,SelectedProduct.Product.BasePacking); ДобавитьВФакт = ДобавитьВФакт -...
```
```csharp
SelectedProduct.Quantity = SelectedLine.Packing.ConvertFrom(ДобавитьВФакт,SelectedProduct.Product.BasePacking) ВсегоОсталосьЗаполнить = ВсегоОстало...
```

### `PackingId.StartsWith`
**Примеры из базы:**
```csharp
SelectedProduct.WithAttributes = SelectedProduct.WithAttributes == true || SelectedProduct.Packing.ПоХарактеристикам == true; SelectedProduct.WithS...
```
```csharp
if (SelectedProduct.PackingId.StartsWith("new")) SelectedProduct.НовШК = SelectedProduct.ШК
```
```csharp
BarcodeData = Temp; ScannedBarcode = BarcodeData.ScannedBarcodeCompatible; SelectedProduct.IsNewBarcode = SelectedProduct.PackingId.StartsWith("new...
```

### `PackingTo.ConvertFrom`
**Примеры из базы:**
```csharp
Quantity = QuantityTo + PackingTo.ConvertFrom(QuantityFrom, PackingFrom)
```

### `PrinterUrl.StartsWith`
**Примеры из базы:**
```csharp
GlobalVars.PrinterUrl.StartsWith("IMP")
```

### `Product.Pack`
**Примеры из базы:**
```csharp
SelectedProduct = СтрокаТовара.Product.Pack(СтрокаТовара.PackingId, 1)
```
```csharp
SelectedProduct= СтрокаСТоваромДокумента.Product.Pack(СтрокаСТоваромДокумента.PackingId, 1)
```
```csharp
SelectedProduct = SelectedLine.Product.Pack(SelectedLine.PackingId, 1); SelectedProduct.Quantity = SelectedLine.DeclaredQuantity - SelectedLine.Cur...
```
```csharp
SelectedProduct = СтрокаКМПлан.Product.Pack(СтрокаКМПлан.PackingId, 1)
```
```csharp
СтрокаКМ = СтрокаКМПлан; SelectedProduct = СтрокаКМ.Product.Pack(СтрокаКМ.PackingId, 1); SelectedProduct.SSCC = СтрокаКМ.SSCC; SelectedProduct.Груп...
```

### `ProductsManager.AddToCache`
**Примеры из базы:**
```csharp
global::Cleverence.Warehouse.ProductsManager.AddToCache(SelectedProduct)
```

### `ProductsManager.FindById`
**Примеры из базы:**
```csharp
ТоварОтбор = global::Cleverence.Warehouse.ProductsManager.FindById(SelectedLine.ИдТовара)
```

### `ProductsManager.FindPackingById`
**Примеры из базы:**
```csharp
УпакОтбор = global::Cleverence.Warehouse.ProductsManager.FindPackingById(SelectedLine.ИдТовара, SelectedLine.ИдЕдиницыИзмерения)
```

### `RegistrationDate.ToString`
**Примеры из базы:**
```csharp
stringBarcode = "(01)" + BarcodeData.GTIN infoFields = new Cleverence.Warehouse.StringCollection() infoFields.Add("(01) " + BarcodeData.GTIN) if (U...
```

### `Result.Add`
**Примеры из базы:**
```csharp
Result = new Cleverence.Warehouse.RowCollection(); Result.Add(info);
```

### `Result.AddRange`
**Примеры из базы:**
```csharp
CurrentTUs = select (*) from Document.ТранспортныеУпаковки where Item.ШтрихкодРодителяТУ == SelectedLine.ШтрихкодТУ; if(CurrentTUs == null || Curre...
```
```csharp
TUs = select (*) from ТранспортныеУпаковки where Item.ШтрихкодРодителяТУ == BarcodeData.BarcodeRaw; Result.AddRange(select (*) from Document.Curren...
```
```csharp
CurrentTUs = select (*) from Document.ТранспортныеУпаковкиФакт where Item.ШтрихкодРодителяТУ == SelectedLine.ШтрихкодТУ; if(CurrentTUs == null || C...
```

### `Rows.Add`
**Примеры из базы:**
```csharp
ТекущаяКоробка = new Cleverence.Warehouse.Row(); ТекущаяКоробка.Ид = BarcodeData.ScannedBarcodeCompatible; ТекущаяКоробка.Родитель = ""; ТекущаяКор...
```
```csharp
ТекущаяПалета = new Cleverence.Warehouse.Row(); ТекущаяПалета.Ид = ТранспортнаяУпаковка != "" ? ТранспортнаяУпаковка.Barcode : ScannedBarcode; Теку...
```
```csharp
ПоискКоробки = new Cleverence.Warehouse.Row(); ПоискКоробки.Ид = BarcodeData.ScannedBarcodeCompatible; ПоискКоробки.Статус = "Закрыта"; ПоискКоробк...
```
```csharp
ПоискПалеты = new Cleverence.Warehouse.Row(); ПоискПалеты.Ид = ТранспортнаяУпаковка.Barcode; ПоискПалета.Родитель == ""; ПоискПалеты.СерийныйНомер ...
```
```csharp
Document.Серии.Rows.Add(Серия)
```

### `Rows.Remove`
**Примеры из базы:**
```csharp
Document.КоробкиПалеты.Rows.Remove(ПроверкаПалет);
```
```csharp
Document.КоробкиПалеты.Rows.Remove(ТекущаяПалета);
```
```csharp
Document.КоробкиПалеты.Rows.Remove(УдалитьКоробку); ТекущаяПалета.Содержит = ТекущаяПалета.Содержит - 1;
```

### `SavedScannedBarcode.Replace`
**Примеры из базы:**
```csharp
BadBarcode = SavedScannedBarcode.Replace("<", "\\<")
```

### `ScannedBarcode.Contains`
**Примеры из базы:**
```csharp
(BarcodeData.IsAlcoMark || ScannedBarcode.Length == 150 || ScannedBarcode.Length == 151 || ScannedBarcode.Length == 68) && ScannedBarcode.Contains(...
```

### `ScannedBarcode.StartsWith`
**Примеры из базы:**
```csharp
ВидМаркировки == "ИСМП" && ScannedBarcode.StartsWith(FNC1) == true
```
```csharp
ScannedBarcode.Length == 84 && ScannedBarcode.StartsWith(Иероглиф) == true
```

### `ScannedBarcode.Substring`
**Примеры из базы:**
```csharp
GO.PlayError(); ScannedBarcodeText = ScannedBarcode.Length>10?ScannedBarcode.Substring(0, 10) + "...'":ScannedBarcode +"'"; ErrorMessage = "Отскани...
```
```csharp
SelectedProduct.ШК = BarcodeData.GTIN; SelectedProduct.СН = ScannedBarcode.Substring(14, 7);
```
```csharp
if (BarcodeData.IsGS1Compatible) SelectedProduct.СН = BarcodeData.GS1.SerialNumber; else if (BarcodeData.IsTobaccoMark) SelectedProduct.СН = Scanne...
```
```csharp
Barcode = "01" + ScannedBarcode.Substring(1)
```
```csharp
ScannedBarcode.Length == 87 && ScannedBarcode.Substring(31, 3) == "GS>"
```

### `ScannedBarcodeCompatible.Substring`
**Примеры из базы:**
```csharp
encoded = BarcodeData.ScannedBarcodeCompatible.Substring(21, 4); PricePerUnit = global::Cleverence.MOTP.Utils.GetMRP(encoded);
```

### `Scanner.EnableDefaultBarcodeTypes`
**Примеры из базы:**
```csharp
Scanner.EnableDefaultBarcodeTypes()
```

### `SelectedLine.Clone`
**Примеры из базы:**
```csharp
TUContains = select (*) from ТранспортныеУпаковки where Item.ШтрихкодРодителяТУ == SelectedLine.ШтрихкодТУ; if (TUContains == null || TUContains.Co...
```
```csharp
Document.ТранспортныеУпаковкиФакт.Add(SelectedLine.Clone());
```
```csharp
currentItems.Add(SelectedLine.Clone())
```

### `SelectedProduct.Clone`
**Примеры из базы:**
```csharp
LastSelectedProduct = SelectedProduct.Clone();
```

### `SelectedProduct.ContainsField`
**Примеры из базы:**
```csharp
SelectedProduct.ContainsField("СтатусПроверкиМарки") && SelectedProduct.СтатусПроверкиМарки == 0
```

### `ShowBarcode.Replace`
**Примеры из базы:**
```csharp
BadBarcode = BadBarcode.Replace(GS, "<b><blue>GS</blue></b>"); BadBarcode = BadBarcode.Replace(FNC1, "<b><blue>FNC1</blue></b>"); BadBarcode = BadB...
```

### `ShowLines.AddCollection`
**Примеры из базы:**
```csharp
ShowLines.AddCollection(select (*) from InventoryItemPrices where Item.ИдХарактеристики == SelectedLine.Ид, SelectedLine.ИмяХарактеристики);
```
```csharp
ShowLines.AddCollection(select (*) from InventoryItemStock where Item.ИдХарактеристики == SelectedLine.Ид, SelectedLine.ИмяХарактеристики);
```
```csharp
ShowLines.AddCollection(select (*) from InventoryItemStock where Item.ИдСерии == SelectedLine.Ид, SelectedLine.ИмяСерии);
```

### `StringOperations.FromBase64`
**Примеры из базы:**
```csharp
result = StringOperations.FromBase64(data)
```

### `StringOperations.ParseByTemplate`
**Примеры из базы:**
```csharp
template = "{GTIN:@[0-9]{14}}{SerialNumber:7}{MRP:4}?{Check:4}?"; parse = StringOperations.ParseByTemplate(BarcodeData.BarcodeRaw, template);
```
```csharp
if (BarcodeData.BarcodeRaw.Length == 150) template = "{Type:@[0-9]{3}}{Series:@[0-9]{3}}{SerialNumber:@[0-9]{8}}{Internal:7}{Check:129}"; else if (...
```
```csharp
template = "{FSRAR:@[0-9]{12}}{Type:@[1-4]{1}}{Line:@[0-9]{2}}{Year:@[0-9]{2}}{Number:@[0-9]{9}}"; parse = StringOperations.ParseByTemplate(Barcode...
```
```csharp
template = "{FSRAR:@[0-9]{12}}{Type:@[1-4]{1}}{Line:@[0-9]{2}}{Year:@[0-9]{2}}{Number:@[0-9]{9}}"; parse = StringOperations.ParseByTemplate(Barcode...
```
```csharp
furTemplate = "{countrycode:@[A-Z]{2}}-{number:@[0-9]{6}}-{code:@[A-Z0-9]{10}}"; IsFurMark = StringOperations.ParseByTemplate(BarcodeData.ScannedBa...
```

### `StringOperations.ToBase64`
**Примеры из базы:**
```csharp
КМBase64 = StringOperations.ToBase64(КМ)
```
```csharp
result = StringOperations.ToBase64(data)
```
```csharp
SelectedProduct.Марка = Barcode; SelectedProduct.ПолнаяМаркаHRI = Barcode; SelectedProduct.ПолнаяМаркаBase64 = StringOperations.ToBase64(BarcodeDat...
```
```csharp
if (Document.ЗаписьПолнойМарки == true && ЭтоБлок == true) { SelectedProduct.ПолныйБлокHRI = BarcodeData.BarcodeGS1Formatted; SelectedProduct.Полны...
```

### `TUs.AddRange`
**Примеры из базы:**
```csharp
CurrentTUs = select (*) from Document.ТранспортныеУпаковки where Item.ШтрихкодРодителяТУ == SelectedLine.ШтрихкодТУ; if(CurrentTUs == null || Curre...
```
```csharp
CurrentTUs = select (*) from Document.ТранспортныеУпаковкиФакт where Item.ШтрихкодРодителяТУ == SelectedLine.ШтрихкодТУ; if(CurrentTUs == null || C...
```

### `TableItems.Add`
**Примеры из базы:**
```csharp
CurrentPackage.Add(tmpPackage); TableItems.Add(tmpPackage);
```

### `TempPacking.ConvertFrom`
**Примеры из базы:**
```csharp
SelectedProduct.Quantity = TempPacking.ConvertFrom(ДобавитьВФакт,SelectedProduct.Product.BasePacking); SelectedProduct.Packing = TempPacking; Selec...
```

### `UnknownProduct.Pack`
**Примеры из базы:**
```csharp
SelectedProduct = UnknownProduct.Pack(); SelectedProduct.Наименование = ScannedBarcode; SelectedProduct.ДанныеДляПечати = ScannedBarcode; SelectedP...
```
```csharp
SelectedProduct = new PackedProduct(ProductLine.ИдТовара, ProductLine.ИдЕдиницыИзмерения); if (SelectedProduct.Product == null || SelectedProduct.P...
```
```csharp
SelectedProduct = UnknownProduct.Pack()
```
```csharp
SelectedProduct = new Cleverence.Warehouse.PackedProduct(ProductLine.ProductId, ProductLine.PackingId); if (SelectedProduct.Product == null || Sele...
```
```csharp
SelectedProduct = UnknownProduct.Pack(); SelectedProduct.ИмяНеизвестного = ИмяНеизвестного; SelectedProduct.Маркировка = Маркировка;
```

### `Utils.GetMRP`
**Примеры из базы:**
```csharp
encoded = BarcodeData.ScannedBarcodeCompatible.Substring(21, 4); PricePerUnit = global::Cleverence.MOTP.Utils.GetMRP(encoded);
```

### `Warehouse.DocumentItemCollection`
**Примеры из базы:**
```csharp
DocumentLines = new Cleverence.Warehouse.DocumentItemCollection(); DocumentLines.AddRange((select (*) from DeclaredItems where Item.CurrentQuantity...
```
```csharp
DeclaredItems = new Cleverence.Warehouse.DocumentItemCollection(); CheckPallet = CurrentItem.SSCC == SelectedProduct.SSCC || CurrentItem.SSCC == ""...
```
```csharp
DocumentLines = new Cleverence.Warehouse.DocumentItemCollection();
```
```csharp
ds_СписокДляВыбора = new Cleverence.Warehouse.DocumentItemCollection();
```
```csharp
if (СтрокиТекущегоТовара == null) СтрокиТекущегоТовара = new Cleverence.Warehouse.DocumentItemCollection()
```

### `Warehouse.DocumentType`
**Примеры из базы:**
```csharp
АлкоОперации = new Cleverence.Warehouse.DocumentType()
```

### `Warehouse.HybridCollection`
**Примеры из базы:**
```csharp
Сумма = new Cleverence.Warehouse.HybridCollection()
```
```csharp
СтрокиПоказа = new Cleverence.Warehouse.HybridCollection()
```

### `Warehouse.ObjectCollection`
**Примеры из базы:**
```csharp
скидки = new Cleverence.Warehouse.ObjectCollection()
```
```csharp
Buffer = new Cleverence.Warehouse.ObjectCollection()
```
```csharp
Buffer = new Cleverence.Warehouse.ObjectCollection(); ПоискВОстатках = new Cleverence.Warehouse.RowCollection(); НайденныеТовары = new Cleverence.W...
```

### `Warehouse.PackedProduct`
**Примеры из базы:**
```csharp
SelectedProduct = new Cleverence.Warehouse.PackedProduct(ProductLine.ProductId, ProductLine.PackingId); if (SelectedProduct.Product == null || Sele...
```
```csharp
if (SelectedLine.ИдТовара != "" && SelectedLine.ИдЕдиницыИзмерения != "") SelectedProduct = new Cleverence.Warehouse.PackedProduct(SelectedLine.ИдТ...
```
```csharp
SelectedProduct = new Cleverence.Warehouse.PackedProduct(SelectedLine.ИдТовара, SelectedLine.ИдЕдиницыИзмерения);
```
```csharp
УпаковкаДляКонвертации = new Cleverence.Warehouse.PackedProduct(SelectedLine.ИдТовара, SelectedLine.ИдЕдиницыИзмерения).Packing
```
```csharp
СтрокаКМ = СтрокаКМОстатки; SelectedProduct = new Cleverence.Warehouse.PackedProduct(СтрокаКМ.ИдТовара, СтрокаКМ.ИдЕдиницыИзмерения); if (SelectedP...
```

### `Warehouse.PackedProductCollection`
**Примеры из базы:**
```csharp
PackedProductsList = new Cleverence.Warehouse.PackedProductCollection()
```

### `Warehouse.Row`
**Примеры из базы:**
```csharp
Строка = new Cleverence.Warehouse.Row()
```
```csharp
ТекущаяКоробка = new Cleverence.Warehouse.Row(); ТекущаяКоробка.Ид = BarcodeData.ScannedBarcodeCompatible; ТекущаяКоробка.Родитель = ""; ТекущаяКор...
```
```csharp
ТекущаяПалета = new Cleverence.Warehouse.Row(); ТекущаяПалета.Ид = ТранспортнаяУпаковка != "" ? ТранспортнаяУпаковка.Barcode : ScannedBarcode; Теку...
```
```csharp
ПоискКоробки = new Cleverence.Warehouse.Row(); ПоискКоробки.Ид = BarcodeData.ScannedBarcodeCompatible; ПоискКоробки.Статус = "Закрыта"; ПоискКоробк...
```
```csharp
ПоискПалеты = new Cleverence.Warehouse.Row(); ПоискПалеты.Ид = ТранспортнаяУпаковка.Barcode; ПоискПалета.Родитель == ""; ПоискПалеты.СерийныйНомер ...
```

### `Warehouse.RowCollection`
**Примеры из базы:**
```csharp
Строки = new Cleverence.Warehouse.RowCollection()
```
```csharp
НетДанных = true; СтрокиТУ = new Cleverence.Warehouse.RowCollection(); СтрокиОстатков = new Cleverence.Warehouse.RowCollection(); СтрокаТУ = Трансп...
```
```csharp
Buffer = new Cleverence.Warehouse.ObjectCollection(); ПоискВОстатках = new Cleverence.Warehouse.RowCollection(); НайденныеТовары = new Cleverence.W...
```
```csharp
ОтображаемаяКоллекция = new Cleverence.Warehouse.RowCollection(); ОтображаемаяКоллекция.AddRange(ОтображаемыеСтроки);
```
```csharp
Result = new Cleverence.Warehouse.RowCollection(); Result.Add(info);
```

### `Warehouse.StringCollection`
**Примеры из базы:**
```csharp
stringBarcode = "(01)" + BarcodeData.GTIN infoFields = new Cleverence.Warehouse.StringCollection() infoFields.Add("(01) " + BarcodeData.GTIN) if (U...
```



<!-- ds-reverse-engineered-syntax-2026-05-20 -->

---

# Mobile SMARTS: правила синтаксиса, обнаруженные при реверс-инжиниринге

Дата фиксации: 2026-05-20

Источник анализа:

- `E:\MobileSmarts\Desktop\Cleverence.Parsing.dll`
- `E:\MobileSmarts\Desktop\Cleverence.MobileSMARTS.Design.dll`
- `E:\MobileSmarts\Server\DataService\Bin\Cleverence.MobileSMARTS.dll`
- `E:\MobileSmarts\Server\DataService\Bin\Cleverence.MobileSMARTS.xml`

Основные классы:

- `Cleverence.Parsing.CompiledExpression`
- `Cleverence.Parsing.CompiledCode`
- `Cleverence.Parsing.Parsers`
- `Cleverence.Parsing.GlobalScope`
- `Cleverence.Warehouse.ActionSession`
- `Cleverence.Warehouse.SessionHelper`
- `Cleverence.Warehouse.Design.ActionSession`

## 1. Движок выражений

Expression-компилятор находится в `Cleverence.Parsing.dll`.

Главный вход:

```csharp
CompiledExpression.Compile(expression).Evaluate(localScope)
```

Для процедурного кода используется:

```csharp
CompiledCode.Compile(code).Evaluate(localScope)
```

В runtime Mobile SMARTS используется `Cleverence.Warehouse.ActionSession`, который реализует `ILocalScope`.

В дизайнере используется отдельный, более бедный scope:

```csharp
Cleverence.Warehouse.Design.ActionSession
```

Поэтому для реального исполнения важнее runtime-класс из `Cleverence.MobileSMARTS.dll`.

## 2. Нормализация выражений

`SessionHelper.EvaluateExpression` перед компиляцией снимает внешние пробелы и фигурные скобки:

```csharp
expression = expression.Trim().TrimStart('{').TrimEnd('}');
```

Поэтому в ряде expression-полей эти записи эквивалентны:

```text
Document.Name
{Document.Name}
```

Для шаблонных строк используется другой путь: `TemplatesParser`.

## 3. Поддержанные операторы expression

Подтверждено грамматикой `Parsers.ExpressionsParser` и `CompiledExpression.Compile`.

```text
+  -  *  /  %
=
==  !=
<   >   <=   >=
&   |
&&  ||
.
,
(...)
```

Поддержан тернарный оператор:

```csharp
condition ? valueIfTrue : valueIfFalse
```

Унарный минус поддержан:

```csharp
-10
-SomeValue
```

Унарный `!` в грамматике и операторах не обнаружен. Практическое правило:

```csharp
// не использовать
!value

// использовать
value == false
value != true
```

## 4. Приоритеты операторов

Чем меньше значение priority, тем выше приоритет в реализации `CompiledExpression`.

```text
. access              1
cast                  2
new                   3
method call           4
* / %                 5
+ -                   6
< <= > >=             8
== !=                 9
&                     10
|                     12
&&                    13
||                    14
?: / select/delete    15
= assignment          16
```

`&&` и `||` реализованы с short-circuit, если `frame.math.LogicImplemented == false`.

## 5. Литералы

Поддержаны:

```csharp
true
false
123
12.34
"text"
```

Целые числа парсятся как `int`.

Числа с точкой парсятся как `Decimal` через `CultureInfo.InvariantCulture`.

Строки пишутся в двойных кавычках.

Подтвержденные escape-последовательности lexer:

```text
\\
\"
\0
\<
\{
\}
```

`null` и `empty` не являются literal в grammar `value`, но поддерживаются через `ActionSession.GetVariableValue`.

## 6. Доступ к переменным

Имя без точки компилируется как доступ к `ILocalScope`:

```csharp
frame.localScope.GetVariableValue(name)
```

Runtime `ActionSession` хранит переменные в `Hashtable` с `StringComparer.InvariantCultureIgnoreCase`.

Имена переменных не чувствительны к регистру.

Фигурные скобки в имени переменной удаляются:

```csharp
name = name.Replace("{", "").Replace("}", "");
```

## 7. Встроенные идентификаторы runtime ActionSession

Подтверждено в `Cleverence.Warehouse.ActionSession.GetVariableValue`.

```text
GO
App
Math
MathOperations
this
item
true
false
null
empty
Document
Products
GlobalVars
Warehouses
CurrentDate
Authorization
ServerContext
UnknownProduct
StringOperations
```

Дополнительно:

- `ItemUid...` ищет строку документа по UID через `Document.FindItemByUid`.
- имя типа документа ищется в `Environment.DocumentTypes`.
- имя таблицы ищется в `Environment.Tables`, возвращается `HybridTable`.

`CurrentDate` нельзя изменить через присваивание:

```csharp
CurrentDate = ...
```

Runtime выбрасывает ошибку:

```text
Текущая дата CurrentDate в сессии не может быть изменена.
```

## 8. SessionKeys

Подтвержденные ключи сессии:

```text
firststorage
secondstorage
selectedproduct
selectedpallet
ssccpallet
selectedline
documentdescription
buffer
localfinished
globalfinished
immediatelyfinished
immediatelyaborted
workflowfinishedonerror
cyclefinished
scannedbarcode
barcodedata
selectedlines
result
message
errormessage
lastsummarydeclared
lastsummarycurrent
lastdifference
ean128
```

Смысл некоторых ключей по XML-документации:

- `selectedline` - текущая строка документа, тип `DocumentItem`.
- `selectedlines` - выбранные строки документа, тип `DocumentItemCollection`.
- `buffer` - буферная зона, тип `DocumentItemCollection`.
- `selectedproduct` - текущий отсканированный объект, тип `PackedProduct`.
- `scannedbarcode` - отсканированный штрихкод.
- `barcodedata` - объект отсканированного штрихкода.

## 9. Чтение свойств

Доступ к свойствам:

```csharp
object.Property
SelectedLine.Quantity
Document.Name
```

Фигурные скобки в имени свойства удаляются:

```csharp
propertyName = propertyName.Replace("{", "").Replace("}", "");
```

Поэтому для `IExpandable` обычно эквивалентны:

```csharp
SelectedLine.SomeField
SelectedLine.{SomeField}
```

Runtime `ActionSession.GetPropertyValue`:

```csharp
return obj is IExpandable
  ? ((IExpandable)obj).GetField(propertyName)
  : Cleverence.Reflection.GetPropertyValue(obj, propertyName);
```

Если объект реализует `IExpandable`, поле читается через `GetField`.

Иначе используется reflection через `Cleverence.Reflection.GetPropertyValue`.

`Cleverence.Reflection.GetPropertyValue` ищет property без учета регистра, включая public/non-public.

## 10. Запись свойств и переменных

Expression поддерживает присваивание:

```csharp
variable = value
object.Property = value
global::Type.StaticProperty = value
```

Присваивание локальной переменной вызывает:

```csharp
localScope.SetVariableValue(name, value)
```

Присваивание свойства вызывает:

```csharp
localScope.SetPropertyValue(obj, propertyName, value)
```

Для `Document`, `DocumentItem`, `Row`, `DocumentItemCollection` runtime дополнительно фиксирует `AssignChange`.

Для `DocumentItemCollection` при наличии колонки в `DocumentType.Columns` значение конвертируется к типу колонки.

Практическое правило: использовать присваивание только в узлах, где оно ожидаемо, например в `AssignAction`, потому что оно имеет побочные эффекты.

## 11. Вызовы методов

Поддержаны:

```csharp
object.Method(arg1, arg2)
global::Type.StaticMethod(arg1, arg2)
LocalFunction(arg1, arg2)
```

Для объекта, реализующего `IMethodCaller`, вызов идет через:

```csharp
IMethodCaller.Invoke(methodName, args)
```

Иначе метод выбирается reflection-ом:

```csharp
Cleverence.Reflection.GetMethod(...)
Cleverence.Reflection.InvokeMethod(...)
```

## 12. Локальные функции runtime ActionSession

Локальная функция - это вызов без объекта:

```csharp
Eval(...)
Is_Of_Type(...)
CDATA(...)
```

В runtime `ActionSession.InvokeFunction` поддерживает:

```csharp
CDATA(...)
```

и любые public instance/static методы самого `ActionSession`.

Подтвержденные методы `ActionSession`, доступные как local functions:

```text
Eval(template)
ProcessTemplate(template)
CalcValue(s)
FindTemplateValue(name)
FindTemplateValue(name, expressionGuaranteed)
EvaluateExpression(expression)
Is_Of_Type(value, typeName)
As_Type(value, typeName)
CDATA(...)
```

`Is_Of_Type(value, typeName)` проверяет:

- .NET-тип через `CompiledExpression.DefaultGlobalScope.TryGetType`.
- тип документа через `Environment.DocumentTypes.FindByName`.
- таблицу через `Environment.Tables.FindByName`.

`As_Type(value, typeName)` приводит объект к типу или возвращает `null`, если приведение невозможно.

## 13. global::

`global::` - это доступ к типу, а не к глобальной функции.

Поддержано:

```csharp
global::System.String.IsNullOrEmpty(value)
global::System.DateTime.Now
global::System.Math.Round(value, 2)
new global::System.DateTime(...)
(global::System.Decimal)value
```

Не поддержано:

```csharp
global::SomeFunction()
```

`GlobalScope.InvokeFunction` всегда выбрасывает:

```text
unknown function 'global::name'
```

Тип через `global::` строится постепенно:

```csharp
global::System.String
global::Cleverence.Warehouse.Document
```

После разрешения типа доступны static property и static method.

## 14. Поиск типов в GlobalScope

`GlobalScope.TryGetType` ищет типы так:

1. применяет алиасы через `Cleverence.Reflection.GetTypeName`;
2. проверяет встроенный cache;
3. вызывает `Type.GetType(name, false, true)`;
4. ищет в `GlobalScope.Usings`;
5. если имя без точки, ищет в default namespaces;
6. вызывает `AssemblyForTypeResolve`, если задан.

Default namespaces:

```text
Cleverence.Warehouse
Cleverence.Warehouse.Compact
Cleverence.MobileSMARTS
Cleverence.Collections
Cleverence.Connectivity
```

Встроенные .NET-типы:

```text
bool
boolean
char
short
ushort
int
int32
uint
long
ulong
float
double
decimal
string
datetime
object
```

Подтвержденные прикладные типы:

```text
Row
Cell
Product
Packing
PackedProduct
Document
DocumentItem
DocumentCollection
DocumentItemCollection
ProductCollection
PackingCollection
PackedProductCollection
ObjectCollection
RowCollection
Dictionary
PathConfiguration
UEObject
Zebra.Zpl
Zebra.Cpcl
```

## 15. Алиасы типов и членов

Runtime `ActionSession.InitializeReflection` добавляет алиасы.

`Product`:

```text
Product == InventoryItem
Product.BasePacking == UnitOfMeasure
Product.BasePackingId == UnitOfMeasureId
Product.Marking == PartNumber
Product.Packings == ItemUnitsOfMeasure
```

`Packing`:

```text
Packing == UnitOfMeasure
Packing.Product == InventoryItem
```

`PackedProduct`:

```text
PackedProduct == InventoryItemWithUnit
PackedProduct == Inventory
PackedProduct.Product == InventoryItem
PackedProduct.Packing == UnitOfMeasure
```

## 16. Ограничения CanCallMethod на сервере

В server-side режиме `CompiledExpression.CanCallMethod` ограничивает опасные вызовы.

Запрещенные или рискованные префиксы:

```text
System.Reflection
System.Diagnostics
System.Data
System.Type
System.Activator
System.Management
System.Messaging
System.ServiceModel
System.Web
System.Runtime
System.Security
System.Net
System.Configuration
System.Environment
System.Enum
System.IO
System.AppDomain
System.CodeDom
System.Threading
System.Console
System.Linq
System.Xml.XmlSerializer
System.Xml.Serialization
System.Delegate
Cleverence.NativeMethods
Cleverence.Parsing
Cleverence.Hosting
Cleverence.Warehouse.DataStorage
Cleverence.Infrastructure
Cleverence.Reflect
Cleverence.Connectivity
Cleverence.Warehouse.WarehouseModel
Cleverence.Warehouse.ActionSession
Cleverence.Warehouse.OneC_
Cleverence.Warehouse.TerminalConnector
Cleverence.ReflectionAliases
Cleverence.Data
Cleverence.Log
Cleverence.Warehouse.Scheduler
Cleverence.MobileSMARTS.API
ICSharpCode.SharpZipLib
Cassini
Microsoft.Win32
Microsoft.Deployment
Microsoft.CSharp
RegistryExtension.RegistryKeyExtensions
Swashbuckle
```

Практическое правило: `global::System.*` не считать универсально доступным. Проверять конкретный тип и метод.

`global::System.String.IsNullOrEmpty(x)` выглядит допустимым, потому что `System.String` не попадает в запрещенные префиксы.

## 17. Индексаторы

Поддержан синтаксис:

```csharp
obj[index]
```

Реализация вызывает:

```csharp
Cleverence.Reflection.InvokeMethod(obj, "get_Item", index)
```

## 18. Null references

Если при доступе к свойству или методу объект равен `null`, поведение зависит от флагов expression:

- `TreatNullReferencesAsNulls` - вернуть `null`;
- `ThrowNullReferences` - бросить `NullReferenceException`;
- по умолчанию выставляется `frame.nullReference = true`, и итоговое выражение возвращает `null`.

## 19. Select и Delete

Expression grammar поддерживает SQL-подобные конструкции:

```text
select first? args from expr as alias? where expr? group by ...? sort by ...?
delete from expr where expr?
```

Примеры формы:

```csharp
select (*) from Products where Quantity > 0
select first (*) from Products where Barcode == scannedbarcode
select (Name, Quantity) from Document.CurrentItems sort by Name asc
select Sum(Quantity) from Document.CurrentItems group by ProductId
delete from SomeTable where Id == 10
```

Выполнение требует `IQueryBuilder`.

В runtime он задается:

```csharp
CompiledExpression.DefaultQueryBuilder = new QueryBuilder();
```

Если `queryBuilder == null`, будет ошибка:

```text
Queries is not supported.
```

## 20. Template grammar

`TemplatesParser` поддерживает:

```text
{expr}
{expr:format}
#[[localization]]#
html-like tags
system format
```

Специальные шаблонные значения:

```text
{null}  -> null
{empty} -> ""
```

Форматированное значение:

```text
{Document.Name}
{CurrentDate:dd.MM.yyyy}
{Quantity:(0,10)}
```

Разрешенные HTML-теги:

```text
r
b
i
u
hr
br
img
```

Также есть обработчик `unknown_html_node`, поэтому неизвестные теги могут обрабатываться отдельно.

Если `FindTemplateValue(name, expressionGuaranteed: false, scope)` получает строку, которая не начинается с `{`, она возвращается как обычный текст, а не вычисляется:

```text
abc -> "abc"
```

## 21. Code grammar

`CompiledCode` поддерживает процедурный код:

```csharp
if (expr) statement
if (expr) { code }
else statement
else { code }

while (expr) statement
while (expr) { code }

return expr;
return;
break;

expr;
```

Важно: это возможности движка `CompiledCode`, а не рекомендация для expression-атрибутов `.mslx`.

Корпоративное правило для редактирования Mobile SMARTS: не писать языковые циклы в `expression`; использовать XML-узел `ForeachAction`.

## 22. Практические запреты и безопасные правила

Не использовать унарный `!`:

```csharp
// плохо
!global::System.String.IsNullOrEmpty(x)

// хорошо
global::System.String.IsNullOrEmpty(x) == false
```

Для системных вызовов использовать полные имена через `global::`, если это требуется проектными правилами:

```csharp
global::System.String.IsNullOrEmpty(x)
global::System.Math.Round(x, 2)
```

Но помнить о server-side ограничениях `CanCallMethod`.

Не использовать `foreach`, `for`, `while` внутри expression-атрибутов `.mslx`, даже если `CompiledCode` технически поддерживает `while`.

Для циклов использовать XML-узел:

```text
ForeachAction
```

Переменная текущей итерации в `ForeachAction` по корпоративному правилу:

```text
SelectedLine
```

## 23. Минимальные примеры выражений

Проверка строки:

```csharp
global::System.String.IsNullOrEmpty(Document.Number) == false
```

Проверка типа:

```csharp
Is_Of_Type(Document, "SomeDocumentType")
```

Приведение типа:

```csharp
As_Type(value, "decimal")
```

Тернарное выражение:

```csharp
Quantity > 0 ? Quantity : 0
```

Доступ к дополнительному полю:

```csharp
SelectedLine.{SomeField}
```

Индексатор:

```csharp
SomeDictionary["Key"]
```

Static method:

```csharp
global::System.Math.Round(Quantity, 2)
```

Static property:

```csharp
global::System.DateTime.Now
```


