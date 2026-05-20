import os
import re
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# === НАСТРОЙКИ ===
OUTPUT_DIR = "Official_Docs"
# CSS-селектор блока, в котором лежит сам текст статьи (чтобы не парсить меню и футер)
# Для большинства сайтов это 'article', 'main' или блок с классом content.
# Возможно, для сайта Cleverence его придется немного уточнить.
CONTENT_SELECTOR = "main" 

# Список URL-адресов статей, которые нужно скачать
URLS_TO_SCRAPE = [
    # Замените эти ссылки на реальные адреса из базы знаний Cleverence
    "https://kb.cleverence.ru/wh15/1.6/what-is-warehouse-15/", 
    "https://kb.cleverence.ru/wh15/1.6/levels-of-warehouse-15/",  
    "https://kb.cleverence.ru/wh15/1.6/how-to-start-working-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/address-storage-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/reference-storage-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/working-with-cells-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/working-with-transport-packaging-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/accounting-by-serial-number-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/accounting-by-series-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/working-with-weighed-goods-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/working-with-retail-object-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/teamwork-with-document-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/printing-labels-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/smart-partial-additional-unloading-of-items-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/mobile-device-monitoring-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/minimum-requirements-for-installing-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-install-warehouse-15-on-pc/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-deploy-a-warehouse-15-database-from-a-template/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-install-warehouse-15-on-android/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-install-warehouse-15-on-smartphone-with-android/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-install-warehouse-15-on-windows/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-connect-mobile-device-with-warehouse-15-to-pc/",
    "https://kb.cleverence.ru/wh15/1.6/mobile-device-does-not-connect-to-pc/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-manually-connect-a-cleverence-database-to-1c/",
    "https://kb.cleverence.ru/wh15/1.6/connecting-to-the-cleverence-database-from-the-1c-server/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-connect-remote-mobile-device-to-warehouse-15-database/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-turn-on-online-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-set-up-directory-exchange-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-update-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-start-with-mobile-device-with-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/receiving-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/pick-and-ship-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/shipment-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/stock-taking-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/write-off-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/goods-return-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/collect-barcodes-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/browse-directories-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/barcode-printing-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/residual-stock-in-cells-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/placement-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/selection-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/aggregation-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/move-to-another-location-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/move-to-another-warehouse-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/packing-list-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/complectation-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/receiving-of-marked-products-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/pick-and-ship-of-marked-products-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/ordering-marking-codes-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/application-of-marking-codes-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/putting-into-circulation-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/write-off-of-marked-codes-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/return-of-marked-goods-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/aggregation-of-marked-goods-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/disaggregation-of-marked-goods-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/printing-duplicate-marking-code/",
    "https://kb.cleverence.ru/wh15/1.6/action-with-marking-code/",
    "https://kb.cleverence.ru/wh15/1.6/what-is-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/receiving-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/pick-and-ship-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/shipment-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/stock-taking-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/write-off-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/collect-barcodes-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/placement-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/selection-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/move-to-another-location-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/move-to-another-warehouse-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/fast-collect-barcodes-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/scan-check-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/main-settings-in-warehouse-15-win-ce/",
    "https://kb.cleverence.ru/wh15/1.6/document-handling-settings-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/what-is-warehouse-15-rfid/",
    "https://kb.cleverence.ru/wh15/1.6/stock-taking-rfid/",
    "https://kb.cleverence.ru/wh15/1.6/rfid-marking/",
    "https://kb.cleverence.ru/wh15/1.6/shipment-rfid/",
    "https://kb.cleverence.ru/wh15/1.6/search-rfid/",
    "https://kb.cleverence.ru/wh15/1.6/receiving-rfid/",
    "https://kb.cleverence.ru/wh15/1.6/binding-of-marking-codes-to-rfid/",
    "https://kb.cleverence.ru/wh15/1.6/integrated-rfid-tags/",
    "https://kb.cleverence.ru/wh15/1.6/settings-warehouse-15-rfid/",
    "https://kb.cleverence.ru/wh15/1.6/settings-on-the-mobile-device-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-delete-diretory-from-mobile-device-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-enter-the-expiration-date-and-production-date-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-choose-a-business-process-on-mobile-device-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-add-a-product-to-document-without-barcode-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-prevent-document-completion-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/what-to-do-with-unknown-barcodes-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-apply-the-same-settings-all-mobile-devices-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-data-exchange-occurs-between-warehouse-15-and-1c/",
    "https://kb.cleverence.ru/wh15/1.6/functionality-of-1c-processing-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/complete-list-supported-1c-configurations-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/alfa-avto-5-1-6-0/",
    "https://kb.cleverence.ru/wh15/1.6/trade-management-10-3-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/trade-management-11-3-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/trade-management-11-4-11-5-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/erp-enterprise-management-2-2-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/erp-enterprise-management-2-4-2-5-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/integrated-automation-2-2-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/integrated-automation-2-4-2-5-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/trading-enterprise-7-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/management-of-our-small-business-1-6-3-0-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/enterprise-accounting-3-0-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/what-is-a-business-process/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-receiving-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-placement-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-shipment-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-selection-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-move-to-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-stock-taking-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-write-off-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-goods-return-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-production-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-complectation-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-packing-list-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-marked-goods-in-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/business-processes-for-goods-commissioning-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/introduction-in-directory-exchange/",
    "https://kb.cleverence.ru/wh15/1.6/uploading-directories-on-the-mobile-device/",
    "https://kb.cleverence.ru/wh15/1.6/adding-new-directories/",
    "https://kb.cleverence.ru/wh15/1.6/directory-exchange-settings/",
    "https://kb.cleverence.ru/wh15/1.6/scheduled-export-of-directories/",
    "https://kb.cleverence.ru/wh15/1.6/introduction-in-exchange-of-documents-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/uploading-documents-to-mobile-device-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/downloading-documents-from-mobile-device-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/regulatory-unloading-of-documents/",
    "https://kb.cleverence.ru/wh15/1.6/document-exchange-settings/",
    "https://kb.cleverence.ru/wh15/1.6/how-customize-document-exchange-window-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/viewing-documents-in-1c/",
    "https://kb.cleverence.ru/wh15/1.6/assigning-document-to-user/",
    "https://kb.cleverence.ru/wh15/1.6/selecting-documents-by-user/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-work-with-one-document-on-several-mobile-devices/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-enable-sound-notification-on-mobile-device/",
    "https://kb.cleverence.ru/wh15/1.6/extension-for-tobacco-products-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-restore-document-from-backup/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-setup-document-truncation-by-comment/",
    "https://kb.cleverence.ru/wh15/1.6/exchange-buttons-in-1c/",
    "https://kb.cleverence.ru/wh15/1.6/send-a-message-to-technical-support/",
    "https://kb.cleverence.ru/wh15/1.6/import-and-manage-users/",
    "https://kb.cleverence.ru/wh15/1.6/printing-labels-and-price-tags/",
    "https://kb.cleverence.ru/wh15/1.6/assigning-barcode-to-document/",
    "https://kb.cleverence.ru/wh15/1.6/working-with-volumetric-and-grade-accounting/",
    "https://kb.cleverence.ru/wh15/1.6/setting-up-database-connection-parameters/",
    "https://kb.cleverence.ru/wh15/1.6/setting-up-retail-objects/",
    "https://kb.cleverence.ru/wh15/1.6/business-process-settings/",
    "https://kb.cleverence.ru/wh15/1.6/sequential-execution-chain-of-business-processes/",
    "https://kb.cleverence.ru/wh15/1.6/setting-global-parameters/",
    "https://kb.cleverence.ru/wh15/1.6/setting-up-global-parameters-for-marking/",
    "https://kb.cleverence.ru/wh15/1.6/advanced-settings/",
    "https://kb.cleverence.ru/wh15/1.6/setting-up-work-with-marking-codes/",
    "https://kb.cleverence.ru/wh15/1.6/export-and-import-of-settings/",
    "https://kb.cleverence.ru/wh15/1.6/1c-configuration-for-working-with-vsd/",
    "https://kb.cleverence.ru/wh15/1.6/connecting-external-handlers/",
    "https://kb.cleverence.ru/wh15/1.6/demo-mode-of-handler/",
    "https://kb.cleverence.ru/wh15/1.6/integration-of-warehouse-15-with-1c-fresh/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-get-new-operations-after-updating/",
    "https://kb.cleverence.ru/wh15/1.6/what-to-do-document-completed-not-appear/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-place-goods-in-storage-cell-in-warehouse/",
    "https://kb.cleverence.ru/wh15/1.6/integration-of-warehouse-15-with-wms-total-logistic/",
    "https://kb.cleverence.ru/wh15/1.6/integration-of-warehouse-15-with-uas-1-4/",
    "https://kb.cleverence.ru/wh15/1.6/integration-of-warehouse-15-with-excel-csv/",
    "https://kb.cleverence.ru/wh15/1.6/cleverence-solution-architecture/",
    "https://kb.cleverence.ru/wh15/1.6/warehouse-15-database-table-structure/",
    "https://kb.cleverence.ru/wh15/1.6/additional-fields-of-the-aggregation-document/",
    "https://kb.cleverence.ru/wh15/1.6/structure-of-additional-document-fields/",
    "https://kb.cleverence.ru/wh15/1.6/structure-of-the-nomenclature-directory/",
    "https://kb.cleverence.ru/wh15/1.6/integration-recommendations-for-1c/",
    "https://kb.cleverence.ru/wh15/1.6/integration-handler/",
    "https://kb.cleverence.ru/wh15/1.6/first-run-of-the-handler/",
    "https://kb.cleverence.ru/wh15/1.6/running-the-handler-in-offline/",
    "https://kb.cleverence.ru/wh15/1.6/running-the-handler-in-online/",
    "https://kb.cleverence.ru/wh15/1.6/calling-arbitrary-functions/",
    "https://kb.cleverence.ru/wh15/1.6/manual-for-organizing-data-exchange/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-display-data-from-1c-on-a-mobile-device/",
    "https://kb.cleverence.ru/wh15/1.6/header-fields-display-settings/",
    "https://kb.cleverence.ru/wh15/1.6/document-search-by-barcode/",
    "https://kb.cleverence.ru/wh15/1.6/document-fill-handler-configuration/",
    "https://kb.cleverence.ru/wh15/1.6/document-exchange-via-custom-code/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-set-up-work-with-labeled-products-in-1c/",
    "https://kb.cleverence.ru/wh15/1.6/1c-integration-manual/",
    "https://kb.cleverence.ru/wh15/1.6/using-com-objects/",
    "https://kb.cleverence.ru/wh15/1.6/data-exchange-via-rest-api/",
    "https://kb.cleverence.ru/wh15/1.6/implementation-of-online-exchange/",
    "https://kb.cleverence.ru/wh15/1.6/ai-support/",
    "https://kb.cleverence.ru/wh15/1.6/introduction-in-web-and-http-services/",
    "https://kb.cleverence.ru/wh15/1.6/cleverence-data-exchange-schemes-via-web-http/",
    "https://kb.cleverence.ru/wh15/1.6/quick-guide-to-setting-up-cleverence-exchange-with-1c-via-web-http/",
    "https://kb.cleverence.ru/wh15/1.6/complete-instruction-for-setting-up-cleverence-exchange-with-1c-via-web-and-http/",
    "https://kb.cleverence.ru/wh15/1.6/connection-setup-with-windows-authentication/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-retrieve-cleverence-objects-in-json-format/",
    "https://kb.cleverence.ru/wh15/1.6/installing-a-web-service-for-1c-versions-below-8.3.9/",
    "https://kb.cleverence.ru/wh15/1.6/how-to-set-up-fastest-possible-online/",
    "https://kb.cleverence.ru/wh15/1.6/glossary-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/faq-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/hints-warnings-and-errors/",
    "https://kb.cleverence.ru/wh15/1.6/1c-handler-errors/",
    "https://kb.cleverence.ru/wh15/1.6/update-history-warehouse-15/",
    "https://kb.cleverence.ru/wh15/1.6/online-with-1c-is-not-working/",
    "https://kb.cleverence.ru/wh15/1.6/incorrect-path-to-file/",
    "https://kb.cleverence.ru/wh15/1.6/document-is-not-writing/",
    "https://kb.cleverence.ru/wh15/1.6/processing-does-not-start-after-update/",
    "https://kb.cleverence.ru/wh15/1.6/marking-codes-are-not-uploaded/",
    "https://kb.cleverence.ru/wh15/1.6/error-in-transferring-markings/",
    "https://kb.cleverence.ru/wh15/1.6/set-up-error-selection-in-1c/",
    "https://kb.cleverence.ru/wh15/1.6/onlex001/",
    "https://kb.cleverence.ru/wh15/1.6/onlex002/",
    "https://kb.cleverence.ru/wh15/1.6/onlex003/",
    "https://kb.cleverence.ru/wh15/1.6/onlex004/",
    "https://kb.cleverence.ru/wh15/1.6/onlex005/",
    "https://kb.cleverence.ru/wh15/1.6/onlex006/",
    "https://kb.cleverence.ru/wh15/1.6/onlex007/",
    "https://kb.cleverence.ru/wh15/1.6/intex001/",
    "https://kb.cleverence.ru/wh15/1.6/mse1005/",
    "https://kb.cleverence.ru/wh15/1.6/1c-crash/"
    

]
# =================

def clean_filename(title):
    """Очищает заголовок от запрещенных символов для создания имени файла"""
    clean_name = re.sub(r'[\\/*?:"<>|]', "", title)
    return clean_name.strip()[:100] # Ограничиваем длину

def fetch_and_convert(url):
    print(f"🔄 Обрабатываю: {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        # МАГИЯ ЗДЕСЬ: используем 'lxml' вместо 'html.parser'
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Безопасно получаем заголовок
        title_tag = soup.find('h1')
        page_title = title_tag.text.strip() if title_tag else "Без_заголовка"
        filename = f"{clean_filename(page_title)}.md"
        
        content_block = soup.select_one(CONTENT_SELECTOR)
        if not content_block:
            content_block = soup.body
            print("  ⚠️ Основной блок не найден, парсим всю страницу.")
            
       # === 1. АГРЕССИВНАЯ ОЧИСТКА ДОМ-ДЕРЕВА ===
        trash_selectors = [
            'nav', 'footer', 
            '.breadcrumb', '.breadcrumbs', '.js-breadcrumbs',
            '.pagination', '.pager', '.page-navigation',
            'img', 'picture', 'svg', 'figure',
            # ДОБАВЛЕНО: Убиваем блоки оглавления (Table of Contents)
            '.toc', '.table-of-contents', '#toc', '.article-toc' 
        ]
        
        # 1. Удаляем все теги по классам
        for selector in trash_selectors:
            for tag in content_block.select(selector):
                tag.decompose()
                
        # ДОБАВЛЕНО: 2. Вырезаем "якоря" из заголовков (Прямая ссылка на...)
        for header in content_block.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            for anchor in header.find_all('a'):
                anchor.decompose()
                
        # ДОБАВЛЕНО: 3. Удаляем абзацы, в которых есть только текст "Содержание этой страницы"
        for p in content_block.find_all(['p', 'div']):
            if p.text.strip() == "Содержание этой страницы":
                p.decompose()

        for a in content_block.find_all('a'):
            a.unwrap()
                
        # Умная конвертация в Markdown
        markdown_text = md(
            str(content_block), 
            strip=['script', 'style'], 
            ignore_links=True
        )
        
        metadata_header = (
            f"Тип_источника: Официальная документация\n"
            f"URL: {url}\n"
            f"Тема: {page_title}\n"
            f"{'='*40}\n\n"
        )
        
        final_text = metadata_header + markdown_text.strip()
        
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_text)
            
        print(f"  ✅ Сохранено: {filename}")
        
    except Exception as e:
        # Теперь исключения перехватываются корректно, не ломая скрипт
        print(f"  ❌ Ошибка при обработке {url}: {e}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 Создана папка {OUTPUT_DIR}")
        
    print(f"🚀 Начинаем сбор базы знаний (Всего статей: {len(URLS_TO_SCRAPE)})")
    for link in URLS_TO_SCRAPE:
        fetch_and_convert(link)
        
    print("\n🎉 Сбор завершен! Файлы лежат в папке Official_Docs")