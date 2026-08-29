import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
from datetime import datetime, timedelta
import math
import difflib
import json
import os
import urllib.parse
import urllib.request
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None
from lunarcalendar import Lunar, Converter
import luming_time_rules as luming_rules
try:
    from lunar_python import Solar as LunarPythonSolar
except Exception:
    LunarPythonSolar = None


COUNTRY_LANGUAGE_MAP = {
    '中国（大陆）': 'zh-CN',
    '中国（非大陆）': 'zh-TW',
    '美国': 'en-US',
    '英国': 'en-GB',
    '日本': 'ja-JP',
    '加拿大': 'en-US',
    '德国': 'de-DE',
    '意大利': 'en-US',
    '西班牙': 'es-ES',
    '荷兰': 'en-US',
    '瑞士': 'de-DE',
    '瑞典': 'en-US',
    '挪威': 'en-US',
    '丹麦': 'en-US',
    '俄罗斯': 'ru-RU',
    '印度': 'en-US',
    '新加坡': 'en-US',
    '马来西亚': 'en-US',
    '泰国': 'en-US',
    '越南': 'en-US',
    '韩国': 'ko-KR',
    '阿联酋': 'ar-SA',
    '沙特阿拉伯': 'ar-SA',
    '埃及': 'ar-SA',
    '巴西': 'pt-BR',
    '墨西哥': 'en-US',
    '阿根廷': 'en-US',
    '南非': 'en-US',
    '新西兰': 'en-US',
    '土耳其': 'en-US',
    '法国': 'fr-FR',
    '澳大利亚': 'en-US',
}

CURRENT_LANG = 'zh-CN'

I18N = {
    'zh-CN': {
        'app_title': '命宫查询（支持农历/阳历）',
        'label_calendar': '输入类型:',
        'radio_solar': '阳历',
        'radio_lunar': '农历',
        'label_gender': '性别:',
        'radio_male': '男',
        'radio_female': '女',
        'label_query_method': '查询方式:',
        'radio_zhiyi': '知易',
        'radio_wenzhen': '问真八字',
        'radio_manual': '手输入八字',
        'label_language': '国家:',
        'label_birthplace': '出生地:',
        'btn_pick_birthplace': '选择出生地',
        'btn_debug_birthplace': '调试出生地',
        'radio_pingqi': '平气法',
        'radio_dingqi': '定气法',
        'check_summer_time': '按夏令时解释输入时间',
        'summer_time_hint': '提示：该日期符合历史夏令时规则，已自动勾选；若出生记录使用标准时，请取消勾选。',
        'query_info': '输入年月日时后后台自动按出生地真太阳时修正并填柱；出生地改为选择模式（国内/国外三级联动）；默认按定气法取月',
        'btn_query': '查询命宫',
        'btn_yuexian': '月限神煞',
        'btn_recalc': '强制重算四柱',
        'selector_title': '选择出生地',
        'selector_cn': '国内',
        'selector_world': '国外',
        'level1_cn': '省份',
        'level2_cn': '城市',
        'level3_cn': '区县',
        'level1_world': '国家',
        'level2_world': '州省',
        'level3_world': '城市',
        'selector_choose_hint': '请选择出生地',
        'selector_current': '当前选择: {name}',
        'btn_ok': '确定',
        'btn_cancel': '取消',
    },
    'zh-TW': {
        'app_title': '命宮查詢（支援農曆/陽曆）',
        'label_calendar': '輸入類型:',
        'radio_solar': '陽曆',
        'radio_lunar': '農曆',
        'label_gender': '性別:',
        'radio_male': '男',
        'radio_female': '女',
        'label_query_method': '查詢方式:',
        'radio_zhiyi': '知易',
        'radio_wenzhen': '問真八字',
        'radio_manual': '手輸入八字',
        'label_language': '國家:',
        'label_birthplace': '出生地:',
        'btn_pick_birthplace': '選擇出生地',
        'btn_debug_birthplace': '調試出生地',
        'radio_pingqi': '平氣法',
        'radio_dingqi': '定氣法',
        'check_summer_time': '按夏令時解釋輸入時間',
        'summer_time_hint': '提示：該日期符合歷史夏令時規則，已自動勾選；若出生記錄使用標準時，請取消勾選。',
        'query_info': '輸入年月日時後後台自動按出生地真太陽時修正並填柱；出生地改為選擇模式（國內/國外三級聯動）；預設按定氣法取月',
        'btn_query': '查詢命宮',
        'btn_yuexian': '月限神煞',
        'btn_recalc': '強制重算四柱',
        'selector_title': '選擇出生地',
        'selector_cn': '國內',
        'selector_world': '國外',
        'level1_cn': '省份',
        'level2_cn': '城市',
        'level3_cn': '區縣',
        'level1_world': '國家',
        'level2_world': '州省',
        'level3_world': '城市',
        'selector_choose_hint': '請選擇出生地',
        'selector_current': '當前選擇: {name}',
        'btn_ok': '確定',
        'btn_cancel': '取消',
    },
    'en-US': {
        'app_title': 'Minggong Query (Solar/Lunar)',
        'label_calendar': 'Calendar:',
        'radio_solar': 'Solar',
        'radio_lunar': 'Lunar',
        'label_gender': 'Gender:',
        'radio_male': 'Male',
        'radio_female': 'Female',
        'label_query_method': 'Method:',
        'radio_zhiyi': 'Zhiyi',
        'radio_wenzhen': 'Wenzhen Bazi',
        'radio_manual': 'Manual Bazi',
        'label_language': 'Country:',
        'label_birthplace': 'Birthplace:',
        'btn_pick_birthplace': 'Select Birthplace',
        'btn_debug_birthplace': 'Debug Birthplace',
        'radio_pingqi': 'Pingqi',
        'radio_dingqi': 'Dingqi',
        'check_summer_time': 'Interpret input as daylight time',
        'summer_time_hint': 'Notice: this date matches a historical daylight-time period and was checked automatically. Clear it if the record uses standard time.',
        'query_info': 'After date/time selection, pillars are auto-adjusted by true solar time. Birthplace is selector-only (domestic/overseas 3-level linkage).',
        'btn_query': 'Query Minggong',
        'btn_yuexian': 'Yuexian ShenSha',
        'btn_recalc': 'Force Recalc Pillars',
        'selector_title': 'Select Birthplace',
        'selector_cn': 'Domestic',
        'selector_world': 'Overseas',
        'level1_cn': 'Province',
        'level2_cn': 'City',
        'level3_cn': 'District',
        'level1_world': 'Country',
        'level2_world': 'State',
        'level3_world': 'City',
        'selector_choose_hint': 'Please select a birthplace',
        'selector_current': 'Selected: {name}',
        'btn_ok': 'OK',
        'btn_cancel': 'Cancel',
    },
    'en-GB': {
        'app_title': 'Minggong Query (Solar/Lunar)',
        'label_calendar': 'Calendar:',
        'radio_solar': 'Solar',
        'radio_lunar': 'Lunar',
        'label_gender': 'Gender:',
        'radio_male': 'Male',
        'radio_female': 'Female',
        'label_query_method': 'Method:',
        'radio_zhiyi': 'Zhiyi',
        'radio_wenzhen': 'Wenzhen Bazi',
        'radio_manual': 'Manual Bazi',
        'label_language': 'Country:',
        'label_birthplace': 'Birthplace:',
        'btn_pick_birthplace': 'Select Birthplace',
        'btn_debug_birthplace': 'Debug Birthplace',
        'radio_pingqi': 'Pingqi',
        'radio_dingqi': 'Dingqi',
        'query_info': 'After date/time selection, pillars are auto-adjusted by true solar time. Birthplace is selector-only (domestic/overseas 3-level linkage).',
        'btn_query': 'Query Minggong',
        'btn_yuexian': 'Yuexian ShenSha',
        'btn_recalc': 'Force Recalc Pillars',
        'selector_title': 'Select Birthplace',
        'selector_cn': 'Domestic',
        'selector_world': 'Overseas',
        'level1_cn': 'Province',
        'level2_cn': 'City',
        'level3_cn': 'District',
        'level1_world': 'Country',
        'level2_world': 'State',
        'level3_world': 'City',
        'selector_choose_hint': 'Please select a birthplace',
        'selector_current': 'Selected: {name}',
        'btn_ok': 'OK',
        'btn_cancel': 'Cancel',
    },
    'fr-FR': {
        'app_title': 'Requete Minggong (Solaire/Lunaire)',
        'label_calendar': 'Calendrier:',
        'radio_solar': 'Solaire',
        'radio_lunar': 'Lunaire',
        'label_gender': 'Genre:',
        'radio_male': 'Homme',
        'radio_female': 'Femme',
        'label_query_method': 'Methode:',
        'radio_zhiyi': 'Zhiyi',
        'radio_wenzhen': 'Wenzhen Bazi',
        'radio_manual': 'Bazi manuel',
        'label_language': 'Pays:',
        'label_birthplace': 'Lieu de naissance:',
        'btn_pick_birthplace': 'Choisir le lieu',
        'btn_debug_birthplace': 'Debug lieu',
        'radio_pingqi': 'Pingqi',
        'radio_dingqi': 'Dingqi',
        'query_info': 'Apres saisie de la date/heure, les piliers sont ajustes automatiquement via le temps solaire vrai. Le lieu est selectionne via un selecteur a 3 niveaux.',
        'btn_query': 'Requete Minggong',
        'btn_yuexian': 'Yuexian ShenSha',
        'btn_recalc': 'Recalculer les piliers',
        'selector_title': 'Choisir le lieu de naissance',
        'selector_cn': 'National',
        'selector_world': 'International',
        'level1_cn': 'Province',
        'level2_cn': 'Ville',
        'level3_cn': 'District',
        'level1_world': 'Pays',
        'level2_world': 'Region',
        'level3_world': 'Ville',
        'selector_choose_hint': 'Veuillez selectionner un lieu',
        'selector_current': 'Selection actuelle: {name}',
        'btn_ok': 'Valider',
        'btn_cancel': 'Annuler',
    },
    'de-DE': {
        'app_title': 'Minggong-Abfrage (Solar/Lunar)',
        'label_calendar': 'Kalender:',
        'radio_solar': 'Solar',
        'radio_lunar': 'Lunar',
        'label_gender': 'Geschlecht:',
        'radio_male': 'Maennlich',
        'radio_female': 'Weiblich',
        'label_query_method': 'Methode:',
        'radio_zhiyi': 'Zhiyi',
        'radio_wenzhen': 'Wenzhen Bazi',
        'radio_manual': 'Manuelles Bazi',
        'label_language': 'Land:',
        'label_birthplace': 'Geburtsort:',
        'btn_pick_birthplace': 'Geburtsort waehlen',
        'btn_debug_birthplace': 'Geburtsort debuggen',
        'radio_pingqi': 'Pingqi',
        'radio_dingqi': 'Dingqi',
        'query_info': 'Nach Eingabe von Datum/Uhrzeit werden die Saeulen automatisch per wahrer Sonnenzeit korrigiert. Der Geburtsort wird ueber einen 3-stufigen Waehler ausgewaehlt.',
        'btn_query': 'Minggong abfragen',
        'btn_yuexian': 'Yuexian ShenSha',
        'btn_recalc': 'Saeulen neu berechnen',
        'selector_title': 'Geburtsort auswaehlen',
        'selector_cn': 'Inland',
        'selector_world': 'Ausland',
        'level1_cn': 'Provinz',
        'level2_cn': 'Stadt',
        'level3_cn': 'Bezirk',
        'level1_world': 'Land',
        'level2_world': 'Bundesland',
        'level3_world': 'Stadt',
        'selector_choose_hint': 'Bitte Geburtsort waehlen',
        'selector_current': 'Aktuelle Auswahl: {name}',
        'btn_ok': 'OK',
        'btn_cancel': 'Abbrechen',
    },
    'es-ES': {
        'app_title': 'Consulta Minggong (Solar/Lunar)',
        'label_calendar': 'Calendario:',
        'radio_solar': 'Solar',
        'radio_lunar': 'Lunar',
        'label_gender': 'Genero:',
        'radio_male': 'Hombre',
        'radio_female': 'Mujer',
        'label_query_method': 'Metodo:',
        'radio_zhiyi': 'Zhiyi',
        'radio_wenzhen': 'Wenzhen Bazi',
        'radio_manual': 'Bazi manual',
        'label_language': 'Pais:',
        'label_birthplace': 'Lugar de nacimiento:',
        'btn_pick_birthplace': 'Seleccionar lugar',
        'btn_debug_birthplace': 'Depurar lugar',
        'radio_pingqi': 'Pingqi',
        'radio_dingqi': 'Dingqi',
        'query_info': 'Despues de ingresar fecha/hora, los pilares se ajustan automaticamente por tiempo solar verdadero. El lugar de nacimiento usa selector de 3 niveles.',
        'btn_query': 'Consultar Minggong',
        'btn_yuexian': 'Yuexian ShenSha',
        'btn_recalc': 'Recalcular pilares',
        'selector_title': 'Seleccionar lugar de nacimiento',
        'selector_cn': 'Nacional',
        'selector_world': 'Extranjero',
        'level1_cn': 'Provincia',
        'level2_cn': 'Ciudad',
        'level3_cn': 'Distrito',
        'level1_world': 'Pais',
        'level2_world': 'Estado',
        'level3_world': 'Ciudad',
        'selector_choose_hint': 'Seleccione un lugar de nacimiento',
        'selector_current': 'Seleccion actual: {name}',
        'btn_ok': 'Aceptar',
        'btn_cancel': 'Cancelar',
    },
    'pt-BR': {
        'app_title': 'Consulta Minggong (Solar/Lunar)',
        'label_calendar': 'Calendario:',
        'radio_solar': 'Solar',
        'radio_lunar': 'Lunar',
        'label_gender': 'Genero:',
        'radio_male': 'Masculino',
        'radio_female': 'Feminino',
        'label_query_method': 'Metodo:',
        'radio_zhiyi': 'Zhiyi',
        'radio_wenzhen': 'Wenzhen Bazi',
        'radio_manual': 'Bazi manual',
        'label_language': 'Pais:',
        'label_birthplace': 'Local de nascimento:',
        'btn_pick_birthplace': 'Selecionar local',
        'btn_debug_birthplace': 'Depurar local',
        'radio_pingqi': 'Pingqi',
        'radio_dingqi': 'Dingqi',
        'query_info': 'Apos inserir data/hora, os pilares sao ajustados automaticamente pelo tempo solar verdadeiro. O local de nascimento usa seletor de 3 niveis.',
        'btn_query': 'Consultar Minggong',
        'btn_yuexian': 'Yuexian ShenSha',
        'btn_recalc': 'Recalcular pilares',
        'selector_title': 'Selecionar local de nascimento',
        'selector_cn': 'Nacional',
        'selector_world': 'Exterior',
        'level1_cn': 'Provincia',
        'level2_cn': 'Cidade',
        'level3_cn': 'Distrito',
        'level1_world': 'Pais',
        'level2_world': 'Estado',
        'level3_world': 'Cidade',
        'selector_choose_hint': 'Selecione um local de nascimento',
        'selector_current': 'Selecao atual: {name}',
        'btn_ok': 'Confirmar',
        'btn_cancel': 'Cancelar',
    },
    'ko-KR': {
        'app_title': '명궁 조회 (양력/음력)',
        'label_calendar': '달력:',
        'radio_solar': '양력',
        'radio_lunar': '음력',
        'label_gender': '성별:',
        'radio_male': '남성',
        'radio_female': '여성',
        'label_query_method': '방식:',
        'radio_zhiyi': 'Zhiyi',
        'radio_wenzhen': 'Wenzhen Bazi',
        'radio_manual': '수동 Bazi',
        'label_language': '국가:',
        'label_birthplace': '출생지:',
        'btn_pick_birthplace': '출생지 선택',
        'btn_debug_birthplace': '출생지 디버그',
        'radio_pingqi': 'Pingqi',
        'radio_dingqi': 'Dingqi',
        'query_info': '날짜/시간 입력 후 진태양시로 자동 보정하여 기둥을 계산합니다. 출생지는 3단계 선택기로 선택합니다.',
        'btn_query': '명궁 조회',
        'btn_yuexian': 'Yuexian ShenSha',
        'btn_recalc': '기둥 강제 재계산',
        'selector_title': '출생지 선택',
        'selector_cn': '국내',
        'selector_world': '해외',
        'level1_cn': '성',
        'level2_cn': '도시',
        'level3_cn': '구/현',
        'level1_world': '국가',
        'level2_world': '주/도',
        'level3_world': '도시',
        'selector_choose_hint': '출생지를 선택하세요',
        'selector_current': '현재 선택: {name}',
        'btn_ok': '확인',
        'btn_cancel': '취소',
    },
    'ru-RU': {
        'app_title': 'Запрос Minggong (Солнечный/Лунный)',
        'label_calendar': 'Календарь:',
        'radio_solar': 'Солнечный',
        'radio_lunar': 'Лунный',
        'label_gender': 'Пол:',
        'radio_male': 'Мужской',
        'radio_female': 'Женский',
        'label_query_method': 'Метод:',
        'radio_zhiyi': 'Zhiyi',
        'radio_wenzhen': 'Wenzhen Bazi',
        'radio_manual': 'Ручной Bazi',
        'label_language': 'Страна:',
        'label_birthplace': 'Место рождения:',
        'btn_pick_birthplace': 'Выбрать место',
        'btn_debug_birthplace': 'Отладка места',
        'radio_pingqi': 'Pingqi',
        'radio_dingqi': 'Dingqi',
        'query_info': 'После ввода даты и времени столпы автоматически корректируются по истинному солнечному времени. Место рождения выбирается через 3-уровневый селектор.',
        'btn_query': 'Запрос Minggong',
        'btn_yuexian': 'Yuexian ShenSha',
        'btn_recalc': 'Пересчитать столпы',
        'selector_title': 'Выбор места рождения',
        'selector_cn': 'Внутри страны',
        'selector_world': 'За рубежом',
        'level1_cn': 'Провинция',
        'level2_cn': 'Город',
        'level3_cn': 'Район',
        'level1_world': 'Страна',
        'level2_world': 'Регион',
        'level3_world': 'Город',
        'selector_choose_hint': 'Выберите место рождения',
        'selector_current': 'Текущий выбор: {name}',
        'btn_ok': 'ОК',
        'btn_cancel': 'Отмена',
    },
    'ar-SA': {
        'app_title': 'استعلام Minggong (شمسي/قمري)',
        'label_calendar': 'التقويم:',
        'radio_solar': 'شمسي',
        'radio_lunar': 'قمري',
        'label_gender': 'الجنس:',
        'radio_male': 'ذكر',
        'radio_female': 'أنثى',
        'label_query_method': 'الطريقة:',
        'radio_zhiyi': 'Zhiyi',
        'radio_wenzhen': 'Wenzhen Bazi',
        'radio_manual': 'Bazi يدوي',
        'label_language': 'الدولة:',
        'label_birthplace': 'مكان الميلاد:',
        'btn_pick_birthplace': 'اختيار المكان',
        'btn_debug_birthplace': 'تصحيح المكان',
        'radio_pingqi': 'Pingqi',
        'radio_dingqi': 'Dingqi',
        'query_info': 'بعد إدخال التاريخ والوقت، يتم ضبط الأعمدة تلقائيا حسب الوقت الشمسي الحقيقي. مكان الميلاد يتم اختياره عبر محدد من 3 مستويات.',
        'btn_query': 'استعلام Minggong',
        'btn_yuexian': 'Yuexian ShenSha',
        'btn_recalc': 'إعادة حساب الأعمدة',
        'selector_title': 'اختيار مكان الميلاد',
        'selector_cn': 'محلي',
        'selector_world': 'خارجي',
        'level1_cn': 'المقاطعة',
        'level2_cn': 'المدينة',
        'level3_cn': 'المنطقة',
        'level1_world': 'الدولة',
        'level2_world': 'الولاية',
        'level3_world': 'المدينة',
        'selector_choose_hint': 'يرجى اختيار مكان الميلاد',
        'selector_current': 'الاختيار الحالي: {name}',
        'btn_ok': 'تأكيد',
        'btn_cancel': 'إلغاء',
    },
    'ja-JP': {
        'app_title': '命宮照会（太陽暦/太陰暦）',
        'label_calendar': '暦:',
        'radio_solar': '太陽暦',
        'radio_lunar': '太陰暦',
        'label_gender': '性別:',
        'radio_male': '男性',
        'radio_female': '女性',
        'label_query_method': '方式:',
        'radio_zhiyi': '知易',
        'radio_wenzhen': '問真八字',
        'radio_manual': '手入力八字',
        'label_language': '国:',
        'label_birthplace': '出生地:',
        'btn_pick_birthplace': '出生地を選択',
        'btn_debug_birthplace': '出生地デバッグ',
        'radio_pingqi': '平気法',
        'radio_dingqi': '定気法',
        'query_info': '日時入力後、真太陽時で自動補正して柱を計算します。出生地は選択式（国内/海外3段連動）です。',
        'btn_query': '命宮を照会',
        'btn_yuexian': '月限神煞',
        'btn_recalc': '四柱を再計算',
        'selector_title': '出生地を選択',
        'selector_cn': '国内',
        'selector_world': '海外',
        'level1_cn': '省',
        'level2_cn': '市',
        'level3_cn': '区県',
        'level1_world': '国',
        'level2_world': '州',
        'level3_world': '都市',
        'selector_choose_hint': '出生地を選択してください',
        'selector_current': '現在の選択: {name}',
        'btn_ok': '確認',
        'btn_cancel': '取消',
    },
}


def t(key):
    pack = I18N.get(CURRENT_LANG, I18N['zh-CN'])
    return pack.get(key, I18N['zh-CN'].get(key, key))


MISC_TEXT = {
    'zh': {
        'unit_year': '年',
        'unit_month': '月',
        'unit_day': '日',
        'unit_hour': '时',
        'label_year_pillar': '年柱:',
        'label_month_pillar': '月柱:',
        'label_day_pillar': '日柱:',
        'label_hour_pillar': '时柱:',
        'label_specified_minggong': '指定命宫:',
        'label_flow_year': '流年年份:',
        'result_frame_title': '查询结果',
        'result_display_area': '结果显示区',
        'table_item': '项目',
    },
    'en': {
        'unit_year': 'Y',
        'unit_month': 'M',
        'unit_day': 'D',
        'unit_hour': 'H',
        'label_year_pillar': 'Year Pillar:',
        'label_month_pillar': 'Month Pillar:',
        'label_day_pillar': 'Day Pillar:',
        'label_hour_pillar': 'Hour Pillar:',
        'label_specified_minggong': 'Specified Minggong:',
        'label_flow_year': 'Flow Year:',
        'result_frame_title': 'Query Result',
        'result_display_area': 'Result Area',
        'table_item': 'Item',
    },
    'ja': {
        'unit_year': '年',
        'unit_month': '月',
        'unit_day': '日',
        'unit_hour': '時',
        'label_year_pillar': '年柱:',
        'label_month_pillar': '月柱:',
        'label_day_pillar': '日柱:',
        'label_hour_pillar': '時柱:',
        'label_specified_minggong': '指定命宮:',
        'label_flow_year': '流年:',
        'result_frame_title': '照会結果',
        'result_display_area': '結果表示エリア',
        'table_item': '項目',
    },
}


def ui_text(key):
    if CURRENT_LANG in ('zh-CN', 'zh-TW'):
        return MISC_TEXT['zh'].get(key, key)
    if CURRENT_LANG == 'ja-JP':
        return MISC_TEXT['ja'].get(key, key)
    return MISC_TEXT['en'].get(key, key)


def ui_month_headers():
    if CURRENT_LANG in ('zh-CN', 'zh-TW'):
        return ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月']
    if CURRENT_LANG == 'ja-JP':
        return ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '臘月']
    return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


RUNTIME_TEXT = {
    'zh': {
        'err_title': '错误',
        'err_address_lib_empty': '地址库为空，请先检查 address_library.json',
        'err_select_three_levels': '请先完成三级选择',
        'err_missing_name': '所选地址缺少 name 字段',
        'err_invalid_datetime': '请填写正确的出生日期和时辰，时辰可输入24小时制格式，如 12:30',
        'err_invalid_datetime_debug': '请先填写正确的出生年月日时，时辰支持如 14:06',
        'err_invalid_lunar': '农历日期无效',
        'err_choose_month_method': '请选择平气法或定气法',
        'err_hour_branch': '时支输入有误',
        'err_hour_text': '时辰输入有误',
        'err_year_stem': '年干输入有误',
        'err_minggong_invalid': '命宫地支无效',
        'err_minggong_calc': '命宫地支无效，无法计算命宫',
        'err_flow_year_number': '流年年份请输入有效数字',
        'err_flow_year_invalid': '流年干支无效，无法计算流年12神',
        'err_flow_month_invalid': '流年年干或月限地支无效，无法计算流月',
        'err_ganzhi_invalid_calc_yuexian': '输入的干支有误，无法计算月限',
        'err_benming_invalid': '本命年柱干支无效，无法计算本命12神',
        'debug_title': '出生地调试',
        'debug_header': '出生地调试信息',
        'debug_raw_input': '原始输入',
        'debug_normalized_input': '清洗后输入',
        'debug_standard_input': '标准时输入',
        'debug_parse_failed': '解析结果: 未识别（将不启用真太阳时）',
        'debug_parse_ok': '解析结果: 已识别 -> {name}',
        'debug_parse_source': '解析来源: {source}',
        'debug_manual_longitude': '经度输入: {longitude:.4f}°E（手动经度）',
        'debug_coords': '匹配坐标: 北纬{latitude:.4f} 东经{longitude:.4f}',
        'debug_true_solar_enabled': '真太阳时启用',
        'debug_yes': '是',
        'debug_no': '否',
        'debug_offset': '修正量',
        'debug_true_time': '修正后时间',
        'debug_match_keys': '包含匹配键(前5)',
        'debug_suggestions': '近似建议(前5)',
        'debug_no_suggestions': '候选建议: 无，可直接输入东经数字(例如 116.4074)',
        'summary_flow_year': '流年',
        'summary_minggong': '命宫',
        'summary_bazi': '八字',
        'summary_standard_time': '标准时',
        'summary_birthplace': '出生地',
        'summary_coords': '地址经纬',
        'summary_longitude': '出生地经度',
        'summary_true_solar_offset': '真太阳时修正量',
        'summary_true_solar_disabled': '未启用（出生地/经度未识别）',
        'summary_true_time': '修正后时间',
        'summary_final_hour': '最终时支',
        'summary_benming_year': '本命年柱',
        'result_title_minggong': '命宫查询结果',
        'result_title_bazi': '八字计算结果',
        'calendar_lunar': '农历',
        'calendar_solar': '阳历',
        'result_input_hint': '输入{calendar}，已自动判断节气',
        'month_line': '月支',
        'year_stem': '年干',
        'hour_branch': '时支',
        'row_flow_month': '流月',
        'row_yuexian': '月限',
        'row_flow_12gong': '流月12宫',
        'row_benming_12gong': '本命12宫',
        'row_benming_suqian': '本命岁前12神',
        'row_benming_maqian': '本命马前12神',
        'row_benming_boshi': '本命博士12神',
        'row_flow_suqian': '流年岁前12神',
        'row_flow_boshi': '流年博士12神',
        'row_flow_maqian': '流年马前12神',
    },
    'en': {
        'err_title': 'Error',
        'err_address_lib_empty': 'Address library is empty. Please check address_library.json first.',
        'err_select_three_levels': 'Please complete all three selection levels first.',
        'err_missing_name': 'The selected address is missing the name field.',
        'err_invalid_datetime': 'Please enter a valid birth date/time. Time supports 24-hour format, e.g. 12:30.',
        'err_invalid_datetime_debug': 'Please enter a valid birth date/time first. Time supports values like 14:06.',
        'err_invalid_lunar': 'Invalid lunar date.',
        'err_choose_month_method': 'Please choose Pingqi or Dingqi month method.',
        'err_hour_branch': 'Invalid hour branch input.',
        'err_hour_text': 'Invalid hour input.',
        'err_year_stem': 'Invalid year stem input.',
        'err_minggong_invalid': 'Invalid Minggong earthly branch.',
        'err_minggong_calc': 'Invalid Minggong earthly branch. Unable to calculate Minggong.',
        'err_flow_year_number': 'Flow year must be a valid number.',
        'err_flow_year_invalid': 'Invalid flow-year Ganzhi. Unable to calculate flow-year 12 gods.',
        'err_flow_month_invalid': 'Invalid flow-year stem or Yuexian branch. Unable to calculate flow months.',
        'err_ganzhi_invalid_calc_yuexian': 'Invalid Ganzhi input. Unable to calculate Yuexian.',
        'err_benming_invalid': 'Invalid natal year pillar. Unable to calculate natal 12 gods.',
        'debug_title': 'Birthplace Debug',
        'debug_header': 'Birthplace Debug Info',
        'debug_raw_input': 'Raw Input',
        'debug_normalized_input': 'Normalized Input',
        'debug_standard_input': 'Standard Time Input',
        'debug_parse_failed': 'Resolve Result: Not recognized (true solar time will be disabled).',
        'debug_parse_ok': 'Resolve Result: Recognized -> {name}',
        'debug_parse_source': 'Resolve Source: {source}',
        'debug_manual_longitude': 'Longitude Input: {longitude:.4f}°E (manual longitude)',
        'debug_coords': 'Matched Coordinates: {latitude:.4f}N, {longitude:.4f}E',
        'debug_true_solar_enabled': 'True Solar Enabled',
        'debug_yes': 'Yes',
        'debug_no': 'No',
        'debug_offset': 'Offset',
        'debug_true_time': 'Corrected Time',
        'debug_match_keys': 'Matched Keys (Top 5)',
        'debug_suggestions': 'Similar Suggestions (Top 5)',
        'debug_no_suggestions': 'No candidate suggestions. You can directly enter a longitude (e.g. 116.4074).',
        'summary_flow_year': 'Flow Year',
        'summary_minggong': 'Minggong',
        'summary_bazi': 'Bazi',
        'summary_standard_time': 'Standard Time',
        'summary_birthplace': 'Birthplace',
        'summary_coords': 'Coordinates',
        'summary_longitude': 'Birthplace Longitude',
        'summary_true_solar_offset': 'True Solar Offset',
        'summary_true_solar_disabled': 'Disabled (birthplace/longitude not recognized)',
        'summary_true_time': 'Corrected Time',
        'summary_final_hour': 'Final Hour Branch',
        'summary_benming_year': 'Natal Year Pillar',
        'result_title_minggong': 'Minggong Query Result',
        'result_title_bazi': 'Bazi Calculation Result',
        'calendar_lunar': 'Lunar',
        'calendar_solar': 'Solar',
        'result_input_hint': 'Input type: {calendar}, solar-term boundary was auto-detected',
        'month_line': 'Month Branch',
        'year_stem': 'Year Stem',
        'hour_branch': 'Hour Branch',
        'row_flow_month': 'Flow Months',
        'row_yuexian': 'Yuexian',
        'row_flow_12gong': 'Flow 12 Palaces',
        'row_benming_12gong': 'Natal 12 Palaces',
        'row_benming_suqian': 'Natal Suqian 12 Gods',
        'row_benming_maqian': 'Natal Maqian 12 Gods',
        'row_benming_boshi': 'Natal Boshi 12 Gods',
        'row_flow_suqian': 'Flow-Year Suqian 12 Gods',
        'row_flow_boshi': 'Flow-Year Boshi 12 Gods',
        'row_flow_maqian': 'Flow-Year Maqian 12 Gods',
    },
    'ja': {
        'err_title': 'エラー',
        'err_address_lib_empty': '住所ライブラリが空です。address_library.json を確認してください。',
        'err_select_three_levels': '3段階の選択を完了してください。',
        'err_missing_name': '選択した住所に name フィールドがありません。',
        'err_invalid_datetime': '生年月日と時刻を正しく入力してください。時刻は 24時間形式（例: 12:30）で入力できます。',
        'err_invalid_datetime_debug': '先に生年月日と時刻を正しく入力してください。時刻は 14:06 のように入力できます。',
        'err_invalid_lunar': '旧暦の日付が無効です。',
        'err_choose_month_method': '平気法または定気法を選択してください。',
        'err_hour_branch': '時支の入力が無効です。',
        'err_hour_text': '時刻の入力が無効です。',
        'err_year_stem': '年干の入力が無効です。',
        'err_minggong_invalid': '命宮地支が無効です。',
        'err_minggong_calc': '命宮地支が無効なため、命宮を計算できません。',
        'err_flow_year_number': '流年は有効な数字で入力してください。',
        'err_flow_year_invalid': '流年の干支が無効なため、流年12神を計算できません。',
        'err_flow_month_invalid': '流年の年干または月限地支が無効なため、流月を計算できません。',
        'err_ganzhi_invalid_calc_yuexian': '入力した干支が無効なため、月限を計算できません。',
        'err_benming_invalid': '本命年柱の干支が無効なため、本命12神を計算できません。',
        'debug_title': '出生地デバッグ',
        'debug_header': '出生地デバッグ情報',
        'debug_raw_input': '入力原文',
        'debug_normalized_input': '正規化後',
        'debug_standard_input': '標準時入力',
        'debug_parse_failed': '解析結果: 未認識（真太陽時は無効になります）',
        'debug_parse_ok': '解析結果: 認識済み -> {name}',
        'debug_parse_source': '解析ソース: {source}',
        'debug_manual_longitude': '経度入力: {longitude:.4f}°E（手動経度）',
        'debug_coords': '一致座標: 北緯{latitude:.4f} 東経{longitude:.4f}',
        'debug_true_solar_enabled': '真太陽時の適用',
        'debug_yes': '有効',
        'debug_no': '無効',
        'debug_offset': '補正量',
        'debug_true_time': '補正後時刻',
        'debug_match_keys': '一致キー（上位5件）',
        'debug_suggestions': '類似候補（上位5件）',
        'debug_no_suggestions': '候補はありません。経度を直接入力できます（例: 116.4074）。',
        'summary_flow_year': '流年',
        'summary_minggong': '命宮',
        'summary_bazi': '八字',
        'summary_standard_time': '標準時',
        'summary_birthplace': '出生地',
        'summary_coords': '座標',
        'summary_longitude': '出生地経度',
        'summary_true_solar_offset': '真太陽時補正',
        'summary_true_solar_disabled': '未適用（出生地/経度を認識できません）',
        'summary_true_time': '補正後時刻',
        'summary_final_hour': '最終時支',
        'summary_benming_year': '本命年柱',
        'result_title_minggong': '命宮照会結果',
        'result_title_bazi': '八字計算結果',
        'calendar_lunar': '旧暦',
        'calendar_solar': '太陽暦',
        'result_input_hint': '入力種別: {calendar}（節気境界を自動判定）',
        'month_line': '月支',
        'year_stem': '年干',
        'hour_branch': '時支',
        'row_flow_month': '流月',
        'row_yuexian': '月限',
        'row_flow_12gong': '流月12宮',
        'row_benming_12gong': '本命12宮',
        'row_benming_suqian': '本命歳前12神',
        'row_benming_maqian': '本命馬前12神',
        'row_benming_boshi': '本命博士12神',
        'row_flow_suqian': '流年歳前12神',
        'row_flow_boshi': '流年博士12神',
        'row_flow_maqian': '流年馬前12神',
    },
}


def rt(key):
    if CURRENT_LANG in ('zh-CN', 'zh-TW'):
        lang_pack = RUNTIME_TEXT['zh']
    elif CURRENT_LANG == 'ja-JP':
        lang_pack = RUNTIME_TEXT['ja']
    else:
        lang_pack = RUNTIME_TEXT['en']
    return lang_pack.get(key, key)


def format_bazi_ascii_box(basic_info, monthly_rows):
    col_widths = [12] + [6] * 12
    months = ["正月", "二月", "三月", "四月", "五月", "六月",
              "七月", "八月", "九月", "十月", "冬月", "腊月"]

    def sep_line(left, mid, right, fill):
        parts = [fill * w for w in col_widths]
        return left + mid.join(parts) + right

    result = ""
    result += sep_line("┌", "┬", "┐", "─") + "\n"
    for label, value in basic_info:
        result += f"│ {label:<10} │ {value:<10} │\n"
    result += sep_line("├", "┼", "┤", "─") + "\n"

    header = ["月\\月份"] + months
    result += "│" + "│".join(f"{c:^{col_widths[i]}}" for i, c in enumerate(header)) + "│\n"
    result += sep_line("├", "┼", "┤", "─") + "\n"

    for label, row in monthly_rows:
        line = [label] + row
        result += "│" + "│".join(f"{line[i]:^{col_widths[i]}}" for i in range(len(line))) + "│\n"

    result += sep_line("└", "┴", "┘", "─") + "\n"
    return result


# 支与干的度数表
dizhi_list = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
tiangan_list = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

branch_cycle = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

from lunarcalendar import solarterm

# 24 节气名单（用于定位中气）
zhongqi_indexes = list(range(2, 25, 2))  # 2,4,...,24

# 获取月支
month_dz_list = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']

# 常用地点经纬度（与真太阳时换算相关，优先匹配更细粒度地名）
LOCATION_COORDS = {
    '湖北省十堰市房县': (32.0547, 110.7358),
    '十堰市房县': (32.0547, 110.7358),
    '房县': (32.0547, 110.7358),
    '湖北省十堰市': (32.6295, 110.7983),
    '十堰市': (32.6295, 110.7983),
    '十堰': (32.6295, 110.7983),
    '新疆乌鲁木齐市沙依巴克区': (43.7944, 87.6317),
    '乌鲁木齐市沙依巴克区': (43.7944, 87.6317),
    '沙依巴克区': (43.7944, 87.6317),
    '新疆乌鲁木齐市天山区': (43.8171, 87.6131),
    '乌鲁木齐市天山区': (43.8171, 87.6131),
    '天山区': (43.8171, 87.6131),
    '乌鲁木齐市': (43.8256, 87.6168),
    '乌鲁木齐': (43.8256, 87.6168),
    '北京': (39.9042, 116.4074),
    '上海': (31.2304, 121.4737),
    '广州': (23.1291, 113.2644),
    '深圳': (22.5431, 114.0579),
}

ADDRESS_LIBRARY_FILE = os.path.join(os.path.dirname(__file__), 'address_library.json')
_ADDRESS_LIBRARY_ENTRIES = []


def _load_address_library():
    global _ADDRESS_LIBRARY_ENTRIES
    _ADDRESS_LIBRARY_ENTRIES = []
    if not os.path.exists(ADDRESS_LIBRARY_FILE):
        return
    try:
        with open(ADDRESS_LIBRARY_FILE, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    except Exception:
        return

    entries = payload.get('entries') if isinstance(payload, dict) else None
    if not isinstance(entries, list):
        return

    for item in entries:
        if not isinstance(item, dict):
            continue
        _ADDRESS_LIBRARY_ENTRIES.append(item)
        name = (item.get('name') or '').strip()
        if not name:
            continue
        try:
            lat = float(item['latitude'])
            lng = float(item['longitude'])
        except Exception:
            # 本地库中无坐标的记录留给后续在线 geocode 兜底
            continue

        LOCATION_COORDS[name] = (lat, lng)
        aliases = item.get('aliases') or []
        if isinstance(aliases, list):
            for alias in aliases:
                alias_text = str(alias).strip()
                if alias_text:
                    LOCATION_COORDS[alias_text] = (lat, lng)


_load_address_library()


def _set_birthplace_text(text):
    if 'entry_birthplace' not in globals():
        return
    entry_birthplace.config(state='normal')
    entry_birthplace.delete(0, tk.END)
    entry_birthplace.insert(0, text)
    entry_birthplace.config(state='readonly')
    refresh_summer_time_suggestion()


def _collect_level_options(entries, key):
    options = set()
    for row in entries:
        value = (row.get(key) or '').strip()
        if value:
            options.add(value)
    return sorted(options)


WORLD_COUNTRY_ZH = {
    'United States': '美国',
    'Japan': '日本',
    'United Kingdom': '英国',
    'France': '法国',
    'Australia': '澳大利亚',
    'Canada': '加拿大',
    'Germany': '德国',
    'Italy': '意大利',
    'Spain': '西班牙',
    'Netherlands': '荷兰',
    'Switzerland': '瑞士',
    'Sweden': '瑞典',
    'Norway': '挪威',
    'Denmark': '丹麦',
    'Russia': '俄罗斯',
    'India': '印度',
    'Singapore': '新加坡',
    'Malaysia': '马来西亚',
    'Thailand': '泰国',
    'Vietnam': '越南',
    'South Korea': '韩国',
    'United Arab Emirates': '阿联酋',
    'Saudi Arabia': '沙特阿拉伯',
    'Egypt': '埃及',
    'Brazil': '巴西',
    'Mexico': '墨西哥',
    'Argentina': '阿根廷',
    'South Africa': '南非',
    'New Zealand': '新西兰',
    'Turkey': '土耳其',
}

WORLD_STATE_ZH = {
    'Capital Region': '首都大区',
    'California': '加利福尼亚州',
    'New York': '纽约州',
    'Washington': '华盛顿州',
    'Texas': '得克萨斯州',
    'Illinois': '伊利诺伊州',
    'England': '英格兰',
    'Scotland': '苏格兰',
    'Ile-de-France': '法兰西岛',
    "Provence-Alpes-Cote d'Azur": '普罗旺斯-阿尔卑斯-蓝色海岸',
    'Occitanie': '奥克西塔尼',
    'Nouvelle-Aquitaine': '新阿基坦',
    'New South Wales': '新南威尔士州',
    'Victoria': '维多利亚州',
    'Queensland': '昆士兰州',
    'Western Australia': '西澳大利亚州',
    'South Australia': '南澳大利亚州',
    'Australian Capital Territory': '首都领地',
}

ALL_STATES_TOKEN = '__ALL_STATES__'


def _is_zh_mode():
    return CURRENT_LANG in ('zh-CN', 'zh-TW')


def _contains_cjk(text):
    if not text:
        return False
    return any('\u4e00' <= ch <= '\u9fff' for ch in str(text))


def _world_country_display(raw_country):
    if not _is_zh_mode():
        return raw_country
    return WORLD_COUNTRY_ZH.get(raw_country, raw_country)


def _world_state_display(raw_state):
    if not _is_zh_mode():
        return raw_state
    return WORLD_STATE_ZH.get(raw_state, raw_state)


def _world_state_display_from_entries(state_raw, entries):
    """中文模式下尽量给州省中文显示：显式映射 > 条目 state_zh > 同名城市中文推断。"""
    if not _is_zh_mode():
        return state_raw

    if state_raw in WORLD_STATE_ZH:
        return WORLD_STATE_ZH[state_raw]

    for row in entries:
        if (row.get('state') or '').strip() != state_raw:
            continue
        state_zh = str(row.get('state_zh') or '').strip()
        if state_zh:
            return state_zh

    for row in entries:
        if (row.get('state') or '').strip() != state_raw:
            continue
        if (row.get('city') or '').strip() != state_raw:
            continue
        inferred = _world_city_display(row)
        if inferred and _contains_cjk(inferred):
            return inferred

    return state_raw


def _world_city_display(entry):
    city = (entry.get('city') or '').strip()
    if not _is_zh_mode():
        return city

    aliases = entry.get('aliases') or []
    if not isinstance(aliases, list):
        aliases = []
    country_zh = _world_country_display((entry.get('country') or '').strip())

    short_cjk = []
    for alias in aliases:
        alias_text = str(alias).strip()
        if not _contains_cjk(alias_text):
            continue
        if country_zh and alias_text.startswith(country_zh) and len(alias_text) > len(country_zh):
            short_cjk.append(alias_text[len(country_zh):])
        else:
            short_cjk.append(alias_text)

    short_cjk = [x for x in short_cjk if x]
    if short_cjk:
        return sorted(short_cjk, key=len)[0]
    return city


def _world_best_birthplace_text(entry):
    """中文模式优先回填中文别名，保证用户看到中文且可被解析。"""
    name = (entry.get('name') or '').strip()
    if not _is_zh_mode():
        return name

    aliases = entry.get('aliases') or []
    if isinstance(aliases, list):
        cjk_aliases = [str(x).strip() for x in aliases if _contains_cjk(str(x).strip())]
        if cjk_aliases:
            country_zh = _world_country_display((entry.get('country') or '').strip())
            for alias in cjk_aliases:
                if country_zh and alias.startswith(country_zh):
                    return alias
            return sorted(cjk_aliases, key=len)[0]
    return name


def _make_display_maps(raw_options, make_display):
    display_to_raw = {}
    ordered_display = []
    for raw in raw_options:
        display = make_display(raw)
        candidate = display
        if candidate in display_to_raw and display_to_raw[candidate] != raw:
            candidate = f'{display} ({raw})'
        display_to_raw[candidate] = raw
        ordered_display.append(candidate)
    return ordered_display, display_to_raw


def apply_language(lang_code):
    global CURRENT_LANG
    if lang_code not in I18N:
        lang_code = 'zh-CN'
    CURRENT_LANG = lang_code

    if 'root' in globals():
        root.title(t('app_title'))

    updates = [
        ('label_calendar', 'label_calendar'),
        ('radio_solar', 'radio_solar'),
        ('radio_lunar', 'radio_lunar'),
        ('label_gender', 'label_gender'),
        ('radio_male', 'radio_male'),
        ('radio_female', 'radio_female'),
        ('label_language', 'label_language'),
        ('label_birthplace', 'label_birthplace'),
        ('btn_pick_birthplace', 'btn_pick_birthplace'),
        ('btn_debug_birthplace', 'btn_debug_birthplace'),
        ('radio_pingqi', 'radio_pingqi'),
        ('radio_dingqi', 'radio_dingqi'),
        ('check_summer_time', 'check_summer_time'),
        ('btn_query', 'btn_query'),
        ('btn_yuexian', 'btn_yuexian'),
        ('btn_recalc_pillars', 'btn_recalc'),
    ]
    for widget_name, text_key in updates:
        widget = globals().get(widget_name)
        if widget is not None:
            widget.config(text=t(text_key))

    info_widget = globals().get('label_query_info')
    if info_widget is not None:
        info_widget.config(text=t('query_info'))

    summer_hint_widget = globals().get('summer_time_hint_label')
    if summer_hint_widget is not None:
        summer_hint_widget.config(text=t('summer_time_hint'))

    misc_updates = [
        ('label_year_unit', 'unit_year'),
        ('label_month_unit', 'unit_month'),
        ('label_day_unit', 'unit_day'),
        ('label_hour_unit', 'unit_hour'),
        ('label_year_pillar', 'label_year_pillar'),
        ('label_month_pillar', 'label_month_pillar'),
        ('label_day_pillar', 'label_day_pillar'),
        ('label_hour_pillar', 'label_hour_pillar'),
        ('label_specified_minggong', 'label_specified_minggong'),
        ('label_flow_year', 'label_flow_year'),
    ]
    for widget_name, text_key in misc_updates:
        widget = globals().get(widget_name)
        if widget is not None:
            widget.config(text=ui_text(text_key))

    frame_widget = globals().get('result_frame')
    if frame_widget is not None:
        frame_widget.config(text=ui_text('result_frame_title'))

    display_widget = globals().get('result_title_label')
    if display_widget is not None and display_widget.cget('text') in ('结果显示区', 'Result Area', '結果表示エリア'):
        display_widget.config(text=ui_text('result_display_area'))

    table_widget = globals().get('result_table')
    if table_widget is not None:
        headers = [ui_text('table_item')] + ui_month_headers()
        for col, title in zip(table_widget['columns'], headers):
            table_widget.heading(col, text=title)


def on_language_select(*_):
    display = language_choice_var.get() if 'language_choice_var' in globals() else ''
    lang = COUNTRY_LANGUAGE_MAP.get(display, 'zh-CN')
    apply_language(lang)


def open_birthplace_selector():
    if not _ADDRESS_LIBRARY_ENTRIES:
        messagebox.showerror(rt('err_title'), rt('err_address_lib_empty'))
        return

    top = tk.Toplevel(root)
    top.title(t('selector_title'))
    top.transient(root)
    top.grab_set()

    region_var = tk.StringVar(value='CN')
    selected_entry = {'item': None}
    level_map = {
        'l1': {},
        'l2': {},
        'l3': {},
    }

    container = tk.Frame(top)
    container.pack(padx=12, pady=10, fill='both', expand=True)

    header = tk.Frame(container)
    header.pack(fill='x', pady=(0, 8))
    radio_region_cn = tk.Radiobutton(header, text=t('selector_cn'), variable=region_var, value='CN')
    radio_region_cn.pack(side='left')
    radio_region_world = tk.Radiobutton(header, text=t('selector_world'), variable=region_var, value='WORLD')
    radio_region_world.pack(side='left', padx=(12, 0))

    level_frame = tk.Frame(container)
    level_frame.pack(fill='x')

    label_l1 = tk.Label(level_frame, text='')
    label_l1.grid(row=0, column=0, sticky='e', padx=(0, 4), pady=4)
    combo_l1 = ttk.Combobox(level_frame, state='readonly', width=20)
    combo_l1.grid(row=0, column=1, sticky='w', pady=4)

    label_l2 = tk.Label(level_frame, text='')
    label_l2.grid(row=0, column=2, sticky='e', padx=(10, 4), pady=4)
    combo_l2 = ttk.Combobox(level_frame, state='readonly', width=20)
    combo_l2.grid(row=0, column=3, sticky='w', pady=4)

    label_l3 = tk.Label(level_frame, text='')
    label_l3.grid(row=0, column=4, sticky='e', padx=(10, 4), pady=4)
    combo_l3 = ttk.Combobox(level_frame, state='readonly', width=20)
    combo_l3.grid(row=0, column=5, sticky='w', pady=4)

    filter_l2_var = tk.StringVar(value='')
    filter_l3_var = tk.StringVar(value='')
    label_filter_l2 = tk.Label(level_frame, text='')
    label_filter_l2.grid(row=1, column=2, sticky='e', padx=(10, 4), pady=(0, 4))
    entry_filter_l2 = tk.Entry(level_frame, textvariable=filter_l2_var, width=22)
    entry_filter_l2.grid(row=1, column=3, sticky='w', pady=(0, 4))
    label_filter_l3 = tk.Label(level_frame, text='')
    label_filter_l3.grid(row=1, column=4, sticky='e', padx=(10, 4), pady=(0, 4))
    entry_filter_l3 = tk.Entry(level_frame, textvariable=filter_l3_var, width=22)
    entry_filter_l3.grid(row=1, column=5, sticky='w', pady=(0, 4))

    options_cache = {
        'l2': [],
        'l3': [],
    }

    preview_var = tk.StringVar(value=t('selector_choose_hint'))
    tk.Label(container, textvariable=preview_var, anchor='w').pack(fill='x', pady=(8, 6))

    def region_entries():
        r = region_var.get()
        return [row for row in _ADDRESS_LIBRARY_ENTRIES if str(row.get('region', '')).upper() == r]

    def resolve_keys_by_region():
        if region_var.get() == 'CN':
            return 'province', 'city', 'district', t('level1_cn'), t('level2_cn'), t('level3_cn')
        return 'country', 'state', 'city', t('level1_world'), t('level2_world'), t('level3_world')

    def filter_caption(level_name):
        if _is_zh_mode():
            return f'{level_name}筛选'
        if CURRENT_LANG == 'ja-JP':
            return f'{level_name}検索'
        return f'Filter {level_name}'

    def _filter_values(options, keyword):
        q = (keyword or '').strip().lower()
        if not q:
            return list(options)
        return [item for item in options if q in str(item).lower()]

    def apply_filter_l2(*_):
        filtered = _filter_values(options_cache['l2'], filter_l2_var.get())
        current = combo_l2.get().strip()
        combo_l2['values'] = filtered
        if current in filtered:
            combo_l2.set(current)
        else:
            combo_l2.set(filtered[0] if filtered else '')
        refresh_l3()

    def apply_filter_l3(*_):
        filtered = _filter_values(options_cache['l3'], filter_l3_var.get())
        current = combo_l3.get().strip()
        combo_l3['values'] = filtered
        if current in filtered:
            combo_l3.set(current)
        else:
            combo_l3.set(filtered[0] if filtered else '')
        refresh_preview()

    def refresh_l1(*_):
        k1, k2, k3, t1, t2, t3 = resolve_keys_by_region()
        label_l1.config(text=f'{t1}:')
        label_l2.config(text=f'{t2}:')
        label_l3.config(text=f'{t3}:')
        label_filter_l2.config(text=f'{filter_caption(t2)}:')
        label_filter_l3.config(text=f'{filter_caption(t3)}:')
        filter_l2_var.set('')
        filter_l3_var.set('')
        rows = region_entries()
        raw_options = _collect_level_options(rows, k1)

        if region_var.get() == 'WORLD':
            display_options, display_map = _make_display_maps(raw_options, _world_country_display)
        else:
            display_options, display_map = _make_display_maps(raw_options, lambda raw: raw)

        level_map['l1'] = display_map
        combo_l1['values'] = display_options
        combo_l1.set(display_options[0] if display_options else '')
        refresh_l2()

    def refresh_l2(*_):
        k1, k2, k3, _, _, _ = resolve_keys_by_region()
        l1_display = combo_l1.get().strip()
        l1_raw = level_map['l1'].get(l1_display, l1_display)

        rows = [row for row in region_entries() if (row.get(k1) or '').strip() == l1_raw]
        raw_options = _collect_level_options(rows, k2)

        if region_var.get() == 'WORLD':
            display_options, display_map = _make_display_maps(
                raw_options,
                lambda raw: _world_state_display_from_entries(raw, rows)
            )
            if _is_zh_mode():
                display_all = '全部州省'
            elif CURRENT_LANG == 'ja-JP':
                display_all = 'すべての州・省'
            else:
                display_all = 'All States'
            display_options = [display_all] + display_options
            display_map = {display_all: ALL_STATES_TOKEN, **display_map}
        else:
            display_options, display_map = _make_display_maps(raw_options, lambda raw: raw)

        level_map['l2'] = display_map
        options_cache['l2'] = list(display_options)
        filter_l3_var.set('')
        apply_filter_l2()

    def refresh_l3(*_):
        k1, k2, k3, _, _, _ = resolve_keys_by_region()

        l1_display = combo_l1.get().strip()
        l2_display = combo_l2.get().strip()
        l1_raw = level_map['l1'].get(l1_display, l1_display)
        l2_raw = level_map['l2'].get(l2_display, l2_display)

        rows = [
            row for row in region_entries()
            if (row.get(k1) or '').strip() == l1_raw
            and (l2_raw == ALL_STATES_TOKEN or (row.get(k2) or '').strip() == l2_raw)
        ]

        raw_options = _collect_level_options(rows, k3)
        if region_var.get() == 'WORLD':
            city_row_map = {}
            for row in rows:
                city_raw = (row.get(k3) or '').strip()
                if city_raw and city_raw not in city_row_map:
                    city_row_map[city_raw] = row
            display_options, display_map = _make_display_maps(
                raw_options,
                lambda raw: _world_city_display(city_row_map.get(raw, {'city': raw}))
            )
        else:
            display_options, display_map = _make_display_maps(raw_options, lambda raw: raw)

        level_map['l3'] = display_map
        options_cache['l3'] = list(display_options)
        apply_filter_l3()

    def refresh_preview(*_):
        k1, k2, k3, _, _, _ = resolve_keys_by_region()
        v1_display = combo_l1.get().strip()
        v2_display = combo_l2.get().strip()
        v3_display = combo_l3.get().strip()
        v1 = level_map['l1'].get(v1_display, v1_display)
        v2 = level_map['l2'].get(v2_display, v2_display)
        v3 = level_map['l3'].get(v3_display, v3_display)
        rows = [
            row for row in region_entries()
            if (row.get(k1) or '').strip() == v1
            and (v2 == ALL_STATES_TOKEN or (row.get(k2) or '').strip() == v2)
            and (row.get(k3) or '').strip() == v3
        ]
        selected_entry['item'] = rows[0] if rows else None
        if selected_entry['item'] is None:
            preview_var.set(t('selector_choose_hint'))
        else:
            if region_var.get() == 'WORLD' and _is_zh_mode():
                item = selected_entry['item']
                country_part = _world_country_display((item.get('country') or '').strip())
                state_part = _world_state_display_from_entries((item.get('state') or '').strip(), region_entries())
                city_part = _world_city_display(item)
                if state_part == (item.get('state') or '').strip() and not _contains_cjk(state_part):
                    display_name = f'{country_part} {city_part}'.strip()
                else:
                    display_name = f'{country_part} {state_part} {city_part}'.strip()
            else:
                display_name = selected_entry['item'].get('name', '')
            preview_var.set(t('selector_current').format(name=display_name))

    def confirm():
        item = selected_entry.get('item')
        if not item:
            messagebox.showerror(rt('err_title'), rt('err_select_three_levels'), parent=top)
            return
        name = (item.get('name') or '').strip()
        if not name:
            messagebox.showerror(rt('err_title'), rt('err_missing_name'), parent=top)
            return
        if region_var.get() == 'WORLD':
            _set_birthplace_text(_world_best_birthplace_text(item))
        else:
            _set_birthplace_text(name)
        update_pillars_from_date()
        top.destroy()

    combo_l1.bind('<<ComboboxSelected>>', refresh_l2)
    combo_l2.bind('<<ComboboxSelected>>', refresh_l3)
    combo_l3.bind('<<ComboboxSelected>>', refresh_preview)
    filter_l2_var.trace_add('write', apply_filter_l2)
    filter_l3_var.trace_add('write', apply_filter_l3)
    region_var.trace_add('write', refresh_l1)

    actions = tk.Frame(container)
    actions.pack(fill='x', pady=(4, 0))
    tk.Button(actions, text=t('btn_ok'), command=confirm).pack(side='right')
    tk.Button(actions, text=t('btn_cancel'), command=top.destroy).pack(side='right', padx=(0, 8))

    refresh_l1()

ENABLE_ONLINE_GEOCODE = True
ONLINE_GEOCODE_TIMEOUT = 1.8
GEOCODE_CACHE_FILE = os.path.join(os.path.dirname(__file__), 'output', 'birthplace_geocode_cache.json')
_BIRTHPLACE_CACHE = {}
_BIRTHPLACE_CACHE_LOADED = False


def normalize_birthplace_text(text):
    if text is None:
        return ''
    normalized = str(text).strip()
    for token in (' ', '\t', '\r', '\n', ',', '，', '。', '·', '、'):
        normalized = normalized.replace(token, '')
    return normalized


def _load_birthplace_cache():
    global _BIRTHPLACE_CACHE_LOADED
    if _BIRTHPLACE_CACHE_LOADED:
        return
    _BIRTHPLACE_CACHE_LOADED = True
    if not os.path.exists(GEOCODE_CACHE_FILE):
        return
    try:
        with open(GEOCODE_CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            _BIRTHPLACE_CACHE.update(data)
    except Exception:
        # 缓存异常不影响主流程
        pass


def _save_birthplace_cache():
    try:
        os.makedirs(os.path.dirname(GEOCODE_CACHE_FILE), exist_ok=True)
        with open(GEOCODE_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(_BIRTHPLACE_CACHE, f, ensure_ascii=False, indent=2)
    except Exception:
        # 缓存保存失败时忽略，不阻断排盘
        pass


def _resolve_from_cache(normalized_text):
    _load_birthplace_cache()
    payload = _BIRTHPLACE_CACHE.get(normalized_text)
    if not isinstance(payload, dict):
        return None
    if payload.get('miss'):
        return {'name': normalized_text, 'latitude': None, 'longitude': None, 'source': 'cache-miss'}
    try:
        lat = float(payload['latitude'])
        lng = float(payload['longitude'])
    except Exception:
        return None
    return {
        'name': payload.get('name') or normalized_text,
        'latitude': lat,
        'longitude': lng,
        'source': 'cache',
    }


def _cache_geocode_hit(normalized_text, name, latitude, longitude):
    _BIRTHPLACE_CACHE[normalized_text] = {
        'name': name,
        'latitude': latitude,
        'longitude': longitude,
    }
    _save_birthplace_cache()


def _cache_geocode_miss(normalized_text):
    _BIRTHPLACE_CACHE[normalized_text] = {'miss': True}
    _save_birthplace_cache()


def _resolve_from_online_geocode(normalized_text):
    if not ENABLE_ONLINE_GEOCODE or not normalized_text:
        return None
    query = urllib.parse.urlencode({
        'format': 'jsonv2',
        'limit': 1,
        'q': normalized_text,
        'accept-language': 'zh-CN',
    })
    url = f'https://nominatim.openstreetmap.org/search?{query}'
    request = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'mingology-kb/1.0 (birthplace geocode)',
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=ONLINE_GEOCODE_TIMEOUT) as resp:
            body = resp.read().decode('utf-8', errors='ignore')
        rows = json.loads(body)
        if not isinstance(rows, list) or not rows:
            return None
        row = rows[0]
        lat = float(row['lat'])
        lng = float(row['lon'])
        name = row.get('display_name') or normalized_text
        return {
            'name': name,
            'latitude': lat,
            'longitude': lng,
            'source': 'online',
        }
    except Exception:
        return None


def resolve_birthplace(text):
    if text is None:
        return None
    raw = text.strip()
    if not raw:
        return None
    normalized = normalize_birthplace_text(raw)
    # 允许直接输入“经度”数字
    try:
        lng = float(normalized)
        if -180 <= lng <= 180:
            return {'name': '手动经度', 'latitude': None, 'longitude': lng, 'source': 'manual-longitude'}
    except ValueError:
        pass

    # 优先匹配更长的地名，避免“乌鲁木齐”提前命中导致区县精度丢失
    for place in sorted(LOCATION_COORDS.keys(), key=len, reverse=True):
        if place in raw or place in normalized:
            lat, lng = LOCATION_COORDS[place]
            return {'name': place, 'latitude': lat, 'longitude': lng, 'source': 'builtin'}

    # 本地缓存命中（含 miss）
    cached = _resolve_from_cache(normalized)
    if cached is not None:
        if cached.get('longitude') is None:
            return None
        return cached

    # 在线地理编码兜底
    online = _resolve_from_online_geocode(normalized)
    if online is not None:
        _cache_geocode_hit(normalized, online['name'], online['latitude'], online['longitude'])
        return online

    # 记住未命中，避免短时间重复请求
    _cache_geocode_miss(normalized)
    return None


def parse_birth_longitude(text):
    info = resolve_birthplace(text)
    if info is None:
        return None
    return info['longitude']


def equation_of_time_minutes(dt):
    """近似均时差（分钟）。"""
    day_of_year = dt.timetuple().tm_yday
    b = math.radians((360 / 365) * (day_of_year - 81))
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)


def to_true_solar_datetime(dt, longitude, timezone_meridian=120.0):
    """将标准时换算为真太阳时。"""
    eot = equation_of_time_minutes(dt)
    longitude_offset = 4.0 * (longitude - timezone_meridian)
    total_offset_minutes = longitude_offset + eot
    return dt + timedelta(minutes=total_offset_minutes), total_offset_minutes


def _is_china_birthplace(text):
    normalized = normalize_birthplace_text(text)
    china_prefixes = (
        '中国', '中國', '北京', '天津', '河北', '山西', '内蒙古', '內蒙古',
        '辽宁', '遼寧', '吉林', '黑龙江', '黑龍江', '上海', '江苏', '江蘇',
        '浙江', '安徽', '福建', '江西', '山东', '山東', '河南', '湖北',
        '湖南', '广东', '廣東', '广西', '廣西', '海南', '重庆', '重慶',
        '四川', '贵州', '貴州', '云南', '雲南', '西藏', '陕西', '陝西',
        '甘肃', '甘肅', '青海', '宁夏', '寧夏', '新疆', '香港', '澳门',
        '澳門', '台湾', '臺灣',
    )
    return normalized.startswith(china_prefixes)


def is_china_summer_time(dt, birthplace_text):
    """Return whether a China civil timestamp falls in the historical DST period."""
    if not _is_china_birthplace(birthplace_text):
        return False
    if ZoneInfo is not None:
        try:
            aware = dt.replace(tzinfo=ZoneInfo('Asia/Shanghai'))
            return bool(aware.dst())
        except Exception:
            pass
    # Fallback for Windows installations without an IANA tzdata package.
    if dt.year == 1986:
        start, end = datetime(1986, 5, 4, 2), datetime(1986, 9, 14, 2)
    elif 1987 <= dt.year <= 1991:
        start = datetime(dt.year, 4, 1) + timedelta(days=(6 - datetime(dt.year, 4, 1).weekday()) % 7)
        end = datetime(dt.year, 9, 1) + timedelta(days=(6 - datetime(dt.year, 9, 1).weekday()) % 7)
        if start.day < 11:
            start += timedelta(days=7)
        if end.day < 11:
            end += timedelta(days=7)
        start = start.replace(hour=2)
        end = end.replace(hour=2)
    else:
        return False
    return start <= dt < end


_SUMMER_TIME_AUTO_KEY = None


def refresh_summer_time_suggestion(*_args):
    """Update the input default when the entered civil date or place changes."""
    global _SUMMER_TIME_AUTO_KEY
    required = ('entry_year', 'entry_month', 'entry_day', 'entry_hour', 'entry_birthplace', 'var', 'summer_time_var')
    if not all(name in globals() for name in required):
        return
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        day = int(entry_day.get())
        time_parts = parse_time_text(entry_hour.get())
        if time_parts is None:
            return
        hour, minute = time_parts
        second = 0
        if var.get() == '农历':
            solar = lunar_to_solar(year, month, day)
            if solar is None:
                return
            year, month, day = solar
        birthplace = entry_birthplace.get()
        key = (year, month, day, hour, minute, second, birthplace)
        if key == _SUMMER_TIME_AUTO_KEY:
            return
        _SUMMER_TIME_AUTO_KEY = key
    except (TypeError, ValueError):
        return

    suggested = is_china_summer_time(datetime(year, month, day, hour, minute, second), birthplace)
    summer_time_var.set(suggested)
    if 'summer_time_hint_label' in globals():
        summer_time_hint_label.config(text=t('summer_time_hint') if suggested else '')
    if 'true_solar_preview_label' in globals():
        update_true_solar_preview()


def update_true_solar_preview(*_args):
    """输入页实时显示真太阳时与地址经纬（与 差异.docx image1 参考图一致）。"""
    if 'true_solar_preview_label' not in globals():
        return
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        day = int(entry_day.get())
        time_parts = parse_time_text(entry_hour.get())
        if time_parts is None:
            raise ValueError
        hour, minute = time_parts
        second = 0
    except (TypeError, ValueError):
        true_solar_preview_label.config(text='')
        return
    if var.get() == '农历':
        solar = lunar_to_solar(year, month, day)
        if solar is None:
            true_solar_preview_label.config(text='')
            return
        year, month, day = solar
    birthplace = entry_birthplace.get().strip()
    if not birthplace:
        true_solar_preview_label.config(text='')
        return
    try:
        ctx = build_true_solar_context(
            year, month, day, hour, minute, birthplace,
            summer_time_var.get() if 'summer_time_var' in globals() else None,
        )
    except Exception:
        true_solar_preview_label.config(text='')
        return
    if not ctx.get('used_true_solar'):
        true_solar_preview_label.config(text='')
        return
    td = ctx['true_dt']
    lat = ctx.get('latitude')
    lon = ctx.get('longitude')
    coords = f'北纬{lat:.4f} 东经{lon:.4f}' if lat is not None and lon is not None else '未识别'
    true_solar_preview_label.config(
        text=f'真太阳时：{td.strftime("%Y-%m-%d %H:%M")}    地址经纬：{coords}'
    )


def format_offset_hhmm(offset_minutes):
    sign = '+' if offset_minutes >= 0 else '-'
    mins = abs(offset_minutes)
    hh = int(mins // 60)
    mm = int(round(mins % 60))
    if mm == 60:
        hh += 1
        mm = 0
    return f'{sign}{hh:02d}:{mm:02d}'


def classify_zi_hour(true_solar_dt):
    """Classify子时 after true-solar correction; the civil date changes at 00:00."""
    if true_solar_dt.hour == 23:
        return '晚子时'
    if true_solar_dt.hour == 0:
        return '早子时'
    return None


def build_true_solar_context(year, month, day, hour, minute, birthplace_text, summer_time_enabled=None, second=0):
    input_dt = datetime(year, month, day, hour, minute, second)
    if summer_time_enabled is None:
        summer_time_enabled = is_china_summer_time(input_dt, birthplace_text)
    standard_dt = input_dt - timedelta(hours=1) if summer_time_enabled else input_dt
    place_info = resolve_birthplace(birthplace_text)
    longitude = place_info['longitude'] if place_info else None
    latitude = place_info['latitude'] if place_info else None
    place_name = place_info['name'] if place_info else None
    if longitude is None:
        true_dt = standard_dt
        offset_minutes = 0.0
        used_true_solar = False
    else:
        true_dt, offset_minutes = to_true_solar_datetime(standard_dt, longitude)
        used_true_solar = True
    return {
        'input_dt': input_dt,
        'standard_dt': standard_dt,
        'summer_time_enabled': bool(summer_time_enabled),
        'true_dt': true_dt,
        'zi_hour_type': classify_zi_hour(true_dt),
        'offset_minutes': offset_minutes,
        'used_true_solar': used_true_solar,
        'longitude': longitude,
        'latitude': latitude,
        'place_name': place_name,
        'birthplace_text': (birthplace_text or '').strip(),
    }


def build_birthplace_debug_lines(year, month, day, hour, minute, birthplace_text):
    raw_text = '' if birthplace_text is None else str(birthplace_text)
    normalized = raw_text.strip()
    place_info = resolve_birthplace(raw_text)
    matched_places = [
        place for place in sorted(LOCATION_COORDS.keys(), key=len, reverse=True)
        if place in normalized
    ]
    suggestions = difflib.get_close_matches(normalized, list(LOCATION_COORDS.keys()), n=5, cutoff=0.35) if normalized else []

    lines = [
        rt('debug_header'),
        f"{rt('debug_raw_input')}: {raw_text or '<empty>'}",
        f"{rt('debug_normalized_input')}: {normalized or '<empty>'}",
        f"{rt('debug_standard_input')}: {year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}",
    ]

    if place_info is None:
        lines.append(rt('debug_parse_failed'))
    else:
        lines.append(rt('debug_parse_ok').format(name=place_info.get('name')))
        lines.append(rt('debug_parse_source').format(source=place_info.get('source', 'unknown')))
        if place_info.get('latitude') is None:
            lines.append(rt('debug_manual_longitude').format(longitude=place_info.get('longitude')))
        else:
            lines.append(rt('debug_coords').format(latitude=place_info.get('latitude'), longitude=place_info.get('longitude')))

    solar_ctx = build_true_solar_context(year, month, day, hour, minute, raw_text)
    lines.append(f"{rt('debug_true_solar_enabled')}: {rt('debug_yes') if solar_ctx['used_true_solar'] else rt('debug_no')}")
    lines.append(f"{rt('debug_offset')}: {format_offset_hhmm(solar_ctx['offset_minutes'])}")
    lines.append(f"{rt('debug_true_time')}: {solar_ctx['true_dt'].strftime('%Y-%m-%d %H:%M')}")

    if matched_places:
        lines.append(f"{rt('debug_match_keys')}: " + '；'.join(matched_places[:5]))
    elif suggestions:
        lines.append(f"{rt('debug_suggestions')}: " + '；'.join(suggestions))
    else:
        lines.append(rt('debug_no_suggestions'))

    return lines


def debug_birthplace():
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        day = int(entry_day.get())
        time_parts = parse_time_text(entry_hour.get())
        if time_parts is None:
            raise ValueError
        hour, minute = time_parts
    except ValueError:
        messagebox.showerror(rt('err_title'), rt('err_invalid_datetime_debug'))
        return

    calendar_type = var.get()
    if calendar_type == '农历':
        solar = lunar_to_solar(year, month, day)
        if solar is None:
            messagebox.showerror(rt('err_title'), rt('err_invalid_lunar'))
            return
        year, month, day = solar

    birthplace_text = entry_birthplace.get() if 'entry_birthplace' in globals() else ''
    lines = build_birthplace_debug_lines(year, month, day, hour, minute, birthplace_text)
    messagebox.showinfo(rt('debug_title'), '\n'.join(lines))


def _format_datetime_cn(dt):
    return f'{dt.year:04d}年{dt.month:02d}月{dt.day:02d}日 {dt.hour:02d}点{dt.minute:02d}分{dt.second:02d}秒'


def _solar_to_datetime(solar_obj):
    return datetime(
        solar_obj.getYear(),
        solar_obj.getMonth(),
        solar_obj.getDay(),
        solar_obj.getHour(),
        solar_obj.getMinute(),
        solar_obj.getSecond(),
    )


def build_zhiyi_extra_info(input_dt, true_dt, gender_text, birthplace_text, month_method):
    """构建与知易界面接近的附加信息（不含命卦）。"""
    if LunarPythonSolar is None:
        return []

    solar = LunarPythonSolar.fromYmdHms(
        true_dt.year,
        true_dt.month,
        true_dt.day,
        true_dt.hour,
        true_dt.minute,
        true_dt.second,
    )
    lunar = solar.getLunar()
    ec = lunar.getEightChar()

    prev_jq = lunar.getPrevJieQi()
    next_jq = lunar.getNextJieQi()

    prev2_name = None
    prev2_dt = None
    try:
        jq_table = lunar.getJieQiTable() or {}
        jq_points = []
        for name, solar_obj in jq_table.items():
            if not isinstance(name, str):
                continue
            if not any('\u4e00' <= ch <= '\u9fff' for ch in name):
                continue
            jq_points.append((name, _solar_to_datetime(solar_obj)))
        jq_points.sort(key=lambda x: x[1])
        for i, (_, dt_val) in enumerate(jq_points):
            if dt_val > true_dt and i >= 2:
                prev2_name, prev2_dt = jq_points[i - 2]
                break
    except Exception:
        prev2_name = None
        prev2_dt = None

    gender_for_yun = 1 if gender_text == '男' else 0
    yun = ec.getYun(gender_for_yun, 2)
    start_solar = yun.getStartSolar()
    start_dt = _solar_to_datetime(start_solar)

    first_dayun = None
    try:
        dayun_list = yun.getDaYun(2)
        if len(dayun_list) > 1:
            first_dayun = dayun_list[1]
    except Exception:
        first_dayun = None

    method_text = month_method if month_method in ('平气法', '定气法') else '定气法'
    lines = [f'根据现代农历{method_text}排盘']
    if prev2_name and prev2_dt:
        lines.append(f'{prev2_name}: {_format_datetime_cn(prev2_dt)}')
    if prev_jq is not None:
        lines.append(f'{prev_jq.getName()}: {_format_datetime_cn(_solar_to_datetime(prev_jq.getSolar()))}')
    lines.append(f'出生: {_format_datetime_cn(input_dt)}')
    if next_jq is not None:
        lines.append(f'{next_jq.getName()}: {_format_datetime_cn(_solar_to_datetime(next_jq.getSolar()))}')

    birthplace_line = (birthplace_text or '').strip()
    if birthplace_line:
        lines.append(f'出生地点: {birthplace_line}')

    lines.append(
        f'起运: 出生后{yun.getStartYear()}年{yun.getStartMonth()}月{yun.getStartDay()}天'
    )
    lines.append(f'      {_format_datetime_cn(start_dt)}')

    if first_dayun is not None:
        dayun_gz = first_dayun.getGanZhi()
        if dayun_gz:
            lines.append(
                f'交运: {start_dt.year}年起入{dayun_gz}运（{first_dayun.getStartAge()}岁）'
            )

    return lines


def calc_dayun_standard(true_dt, gender_text, sect=2, count=10):
    """普通排盘·大运：直接调用 lunar_python 官方起运/大运计算，不叠加任何自研规则。"""
    if LunarPythonSolar is None:
        return None

    solar = LunarPythonSolar.fromYmdHms(
        true_dt.year, true_dt.month, true_dt.day,
        true_dt.hour, true_dt.minute, true_dt.second,
    )
    lunar = solar.getLunar()
    ec = lunar.getEightChar()
    gender_for_yun = 1 if gender_text == '男' else 0
    yun = ec.getYun(gender_for_yun, sect)
    start_dt = _solar_to_datetime(yun.getStartSolar())

    dayun_rows = []
    for du in yun.getDaYun(count + 1):  # index 0 是起运前的阶段，跳过，只取真正的大运
        if du.getIndex() < 1:
            continue
        dayun_rows.append({
            'index': du.getIndex(),
            'ganzhi': du.getGanZhi(),
            'start_age': du.getStartAge(),
            'end_age': du.getEndAge(),
            'start_year': du.getStartYear(),
            'end_year': du.getEndYear(),
        })

    return {
        'forward': yun.isForward(),
        'start_year': yun.getStartYear(),
        'start_month': yun.getStartMonth(),
        'start_day': yun.getStartDay(),
        'start_hour': yun.getStartHour(),
        'start_date': start_dt,
        'dayun': dayun_rows,
    }


def calc_bazi_pillars_with_true_solar(year, month, day, hour, minute, birthplace_text, summer_time_enabled=None):
    """按出生地真太阳时计算四柱；地点或精算库不可用时拒绝排盘。"""
    solar_ctx = build_true_solar_context(year, month, day, hour, minute, birthplace_text, summer_time_enabled)
    true_dt = solar_ctx['true_dt']

    if not solar_ctx['used_true_solar']:
        raise ValueError('出生地未解析，不能使用真太阳时排盘')
    if LunarPythonSolar is None:
        raise RuntimeError('lunar_python 不可用，不能计算精确四柱')

    solar = LunarPythonSolar.fromYmdHms(true_dt.year, true_dt.month, true_dt.day, true_dt.hour, true_dt.minute, true_dt.second)
    ec = solar.getLunar().getEightChar()
    return {
        'year_pillar': ec.getYear(),
        'month_pillar': ec.getMonth(),
        'day_pillar': ec.getDay(),
        'hour_pillar': ec.getTime(),
        'solar_ctx': solar_ctx,
        'source': 'lunar_python',
    }


def get_month_dz_from_datetime(dt):
    """按具体时刻取月支，优先使用精算月柱，回退到原日期逻辑。"""
    if LunarPythonSolar is not None:
        solar = LunarPythonSolar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        month_pillar = solar.getLunar().getEightChar().getMonth()
        _, month_dz = parse_pillar(month_pillar)
        month_num = get_dizhi_num(month_dz) if month_dz else None
        if month_dz and month_num is not None:
            return month_dz, month_num
    month_dz, month_num = get_month_dz(dt.year, dt.month, dt.day)
    if month_dz and month_num is not None:
        return month_dz, month_num
    return None, None

def get_dizhi_num(dz):
    try:
        return dizhi_list.index(dz) + 1
    except ValueError:
        return None

def get_tiangan_num(tg):
    try:
        return tiangan_list.index(tg) + 1
    except ValueError:
        return None

def dizhi_by_num(num):
    return dizhi_list[(num - 1) % 12]

def tiangan_by_num(num):
    return tiangan_list[(num - 1) % 10]

# 表格格式化工具
def format_12col_table(rows):
    month_names = ['正月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
    header = ['月'] + month_names
    table = [header] + [[label] + row for label, row in rows]
    col_widths = [max(len(str(cell)) for cell in column) + 2 for column in zip(*table)]
    lines = []
    lines.append(''.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(header)))
    lines.append(''.join('-' * col_widths[i] for i in range(len(col_widths))))
    for label, row in rows:
        line = str(label).ljust(col_widths[0])
        for i, cell in enumerate(row, 1):
            line += str(cell).ljust(col_widths[i])
        lines.append(line)
    return '\n'.join(lines)

# ---------------------------------------------------------------------------
# 十神（参照图 image6/image9：大运网格每个流年格显示“天干十神 + 地支本气十神”两字简写）
# ---------------------------------------------------------------------------
TIANGAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
}
# 地支本气（藏干主气）
DIZHI_MAIN_QI = {
    '子': '癸', '丑': '己', '寅': '甲', '卯': '乙', '辰': '戊', '巳': '丙',
    '午': '丁', '未': '己', '申': '庚', '酉': '辛', '戌': '戊', '亥': '壬',
}
_WX_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}  # 我生
_WX_KE = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}  # 我克

TEN_GOD_NAMES = ['比肩', '劫财', '食神', '伤官', '偏财', '正财', '七杀', '正官', '偏印', '正印']
TEN_GOD_ABBR = {
    '比肩': '比', '劫财': '劫', '食神': '食', '伤官': '伤',
    '偏财': '才', '正财': '财', '七杀': '杀', '正官': '官',
    '偏印': '枭', '正印': '印',
}
TEN_GOD_COLORS = {
    '比肩': '#2F5597', '劫财': '#5B9BD5',
    '食神': '#00B050', '伤官': '#538135',
    '偏财': '#C55A11', '正财': '#E36C09',
    '七杀': '#C00000', '正官': '#FF0000',
    '偏印': '#7030A0', '正印': '#8064A2',
}


def calc_stem_ten_god(day_stem, target_stem):
    """目标天干相对日主的十神（标准十神表：同五行比劫；我生食伤；我克财；克我官杀；生我印）。"""
    if day_stem not in TIANGAN_WUXING or target_stem not in TIANGAN_WUXING:
        return ''
    dw = TIANGAN_WUXING[day_stem]
    tw = TIANGAN_WUXING[target_stem]
    same_polarity = (day_stem in YANG_TIANGAN) == (target_stem in YANG_TIANGAN)
    if dw == tw:
        return '比肩' if same_polarity else '劫财'
    if _WX_SHENG[dw] == tw:
        return '食神' if same_polarity else '伤官'
    if _WX_KE[dw] == tw:
        return '偏财' if same_polarity else '正财'
    if _WX_KE[tw] == dw:
        return '七杀' if same_polarity else '正官'
    if _WX_SHENG[tw] == dw:
        return '偏印' if same_polarity else '正印'
    return ''


def calc_flow_year_ten_god(day_stem, year_ganzhi):
    """流年格十神对：返回 (天干十神, 地支本气十神)，与参照图“杀食/才枭/财印”等两字简写格式对应。"""
    if not day_stem or not year_ganzhi or len(year_ganzhi) < 2:
        return ('', '')
    tg_god = calc_stem_ten_god(day_stem, year_ganzhi[0])
    main_qi = DIZHI_MAIN_QI.get(year_ganzhi[1])
    dz_god = calc_stem_ten_god(day_stem, main_qi) if main_qi else ''
    return (tg_god, dz_god)

# 岁前十二神定义
SUQIAN_12SHEN_NAMES = ['太岁', '太阳', '丧门', '太阴', '官符', '死符', '岁破', '龙德', '白虎', '福星', '吊客', '病符']

SHEN_SHA_PAIRS = {
    '太岁': ['伏尸', '剑锋'],
    '太阳': ['天空', '青龙'],
    '丧门': ['地雌'],
    '太阴': ['勾绞'],
    '官符': ['五鬼'],
    '死符': ['小耗'],
    '岁破': ['大耗'],
    '龙德': ['紫微'],
    '白虎': ['天雄', '飞廉'],
    '福星': ['福德', '披麻'],
    '吊客': ['天狗'],
    '病符': ['陌越'],
}

# 马前十二神定义
MAQIAN_12SHEN_NAMES = ['天煞', '地煞', '年煞', '月煞', '亡神', '将星', '攀鞍', '驿马', '六厄', '华盖', '劫煞', '灾煞']
MAQIAN_12SHEN_STAGES = ['养地', '长生', '败地', '冠带', '临官', '帝旺', '衰地', '病地', '死地', '墓库', '绝地', '胎地']

# 计算马前十二神：以年支局五行的养地为1天煞，长生为2地煞
# start_branch 应为对应“养地”的那一支
# 例如，若年支局五行的养地对应某地支，则从该支开始排出十二神

def calc_maqian_12shen(start_branch):
    idx = get_branch_index(start_branch)
    if idx is None:
        return None
    result = []
    for i, shen in enumerate(MAQIAN_12SHEN_NAMES):
        branch = branch_cycle[(idx + i) % 12]
        stage = MAQIAN_12SHEN_STAGES[i]
        result.append((branch, shen, stage))
    return result

MAQIAN_YANGDI_BY_BRANCH = {
    '寅': '丑', '午': '丑', '戌': '丑',
    '巳': '辰', '酉': '辰', '丑': '辰',
    '申': '未', '子': '未', '辰': '未',
    '亥': '戌', '卯': '戌', '未': '戌',
}

def get_maqian_start_branch_for_year_branch(year_branch):
    if year_branch is None:
        return None
    return MAQIAN_YANGDI_BY_BRANCH.get(year_branch.strip())

def calc_maqian_12shen_for_year_branch(year_branch):
    start_branch = get_maqian_start_branch_for_year_branch(year_branch)
    if start_branch is None:
        return None
    return calc_maqian_12shen(start_branch)

BOSHI_12SHEN_NAMES = ['博士', '力士', '青龙', '小耗', '将军', '奏书', '飞廉', '喜神', '病符', '大耗', '伏兵', '官府']
BOSHI_LU_BRANCH = {
    '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午', '戊': '辰',
    '己': '未', '庚': '申', '辛': '酉', '壬': '亥', '癸': '子',
}

# 阳年顺排，阴年逆排
YANG_TIANGAN = {'甲', '丙', '戊', '庚', '壬'}
YIN_TIANGAN = {'乙', '丁', '己', '辛', '癸'}

# 计算博士十二神：以年干禄所在支为博士起点，阳年顺排，阴年逆排
# 例如丙午年：丙禄在巳，丙为阳年顺排；乙巳年：乙禄在卯，乙为阴年逆排

def calc_boshi_12shen(year_tg):
    year_tg = year_tg.strip()
    start_branch = BOSHI_LU_BRANCH.get(year_tg)
    if start_branch is None:
        return None
    direction = 1 if year_tg in YANG_TIANGAN else -1
    idx = get_branch_index(start_branch)
    if idx is None:
        return None
    result = []
    for i, shen in enumerate(BOSHI_12SHEN_NAMES):
        branch = branch_cycle[(idx + direction * i) % 12]
        result.append((branch, shen))
    return result

# 计算岁前十二神：以年地支起太岁，依序展开12个地支
# 例如丙午年起午为太岁，下一支未为太阳，依次类推
def calc_suqian_12shen(start_branch):
    idx = get_branch_index(start_branch)
    if idx is None:
        return None
    result = []
    for i, shen in enumerate(SUQIAN_12SHEN_NAMES):
        branch = branch_cycle[(idx + i) % 12]
        result.append((branch, shen))
    return result

# 计算命宫地支
def calc_minggong_dizhi(month_num, hour_dz):
    h = get_dizhi_num(hour_dz)
    if h is None:
        return None
    s = month_num + h
    # 参考公式：以 26 去减它们的和（与文档“14或26”一致），若结果超出 12 则循环
    s = 26 - s
    while s <= 0:
        s += 12
    while s > 12:
        s -= 12
    return dizhi_by_num(s)

# 计算命宫天干（五虎遁）
def get_wuhu_start_tiangan(year_tg):
    y = get_tiangan_num(year_tg)
    if y is None:
        return None
    # 五虎遁：甲己丙，乙庚戊，丙辛庚，丁壬壬，戊癸甲
    mapping = {
        1: 3, 6: 3,  # 甲/己 -> 丙
        2: 5, 7: 5,  # 乙/庚 -> 戊
        3: 7, 8: 7,  # 丙/辛 -> 庚
        4: 9, 9: 9,  # 丁/壬 -> 壬
        5: 1, 10: 1, # 戊/癸 -> 甲
    }
    return mapping.get(y)


def calc_minggong_tiangan(year_tg, minggong_dz):
    start = get_wuhu_start_tiangan(year_tg)
    d = get_dizhi_num(minggong_dz)
    if start is None or d is None:
        return None
    # 支位从寅开始算起（寅=1）
    offset = d - 1
    s = start + offset
    while s > 10:
        s -= 10
    return tiangan_by_num(s)

# 计算月限起点地支
def calc_yuexian_start_branch(birth_year_dz, tai_sui_dz, minggong_dz):
    birth_idx = get_dizhi_num(birth_year_dz)
    tai_idx = get_dizhi_num(tai_sui_dz)
    ming_idx = get_dizhi_num(minggong_dz)
    if birth_idx is None or tai_idx is None or ming_idx is None:
        return None
    # 以流年太岁与命宫的相距位数，后退出生年支得到正月起点
    distance = (tai_idx - ming_idx) % 12
    start_idx = birth_idx - distance
    while start_idx <= 0:
        start_idx += 12
    return dizhi_by_num(start_idx)

# 五虎遁月干：根据流年年干和月限地支直接查表
# 甲己年：寅丙、卯丁、辰戊、巳己、午庚、未辛、申壬、酉癸、戌甲、亥乙、子丙、丑丁
# 乙庚年：寅戊、卯己、辰庚、巳辛、午壬、未癸、申甲、酉乙、戌丙、亥丁、子戊、丑己
# 丙辛年：寅庚、卯辛、辰壬、巳癸、午甲、未乙、申丙、酉丁、戌戊、亥己、子庚、丑辛
# 丁壬年：寅壬、卯癸、辰甲、巳乙、午丙、未丁、申戊、酉己、戌庚、亥辛、子壬、丑癸
# 戊癸年：寅甲、卯乙、辰丙、巳丁、午戊、未己、申庚、酉辛、戌壬、亥癸、子甲、丑乙

def get_wuhu_dun_month_tiangan(year_tg, month_branch):
    year_tg = year_tg.strip()
    month_branch = month_branch.strip()
    mapping = {
        '甲': {'寅':'丙','卯':'丁','辰':'戊','巳':'己','午':'庚','未':'辛','申':'壬','酉':'癸','戌':'甲','亥':'乙','子':'丙','丑':'丁'},
        '己': {'寅':'丙','卯':'丁','辰':'戊','巳':'己','午':'庚','未':'辛','申':'壬','酉':'癸','戌':'甲','亥':'乙','子':'丙','丑':'丁'},
        '乙': {'寅':'戊','卯':'己','辰':'庚','巳':'辛','午':'壬','未':'癸','申':'甲','酉':'乙','戌':'丙','亥':'丁','子':'戊','丑':'己'},
        '庚': {'寅':'戊','卯':'己','辰':'庚','巳':'辛','午':'壬','未':'癸','申':'甲','酉':'乙','戌':'丙','亥':'丁','子':'戊','丑':'己'},
        '丙': {'寅':'庚','卯':'辛','辰':'壬','巳':'癸','午':'甲','未':'乙','申':'丙','酉':'丁','戌':'戊','亥':'己','子':'庚','丑':'辛'},
        '辛': {'寅':'庚','卯':'辛','辰':'壬','巳':'癸','午':'甲','未':'乙','申':'丙','酉':'丁','戌':'戊','亥':'己','子':'庚','丑':'辛'},
        '丁': {'寅':'壬','卯':'癸','辰':'甲','巳':'乙','午':'丙','未':'丁','申':'戊','酉':'己','戌':'庚','亥':'辛','子':'壬','丑':'癸'},
        '壬': {'寅':'壬','卯':'癸','辰':'甲','巳':'乙','午':'丙','未':'丁','申':'戊','酉':'己','戌':'庚','亥':'辛','子':'壬','丑':'癸'},
        '戊': {'寅':'甲','卯':'乙','辰':'丙','巳':'丁','午':'戊','未':'己','申':'庚','酉':'辛','戌':'壬','亥':'癸','子':'甲','丑':'乙'},
        '癸': {'寅':'甲','卯':'乙','辰':'丙','巳':'丁','午':'戊','未':'己','申':'庚','酉':'辛','戌':'壬','亥':'癸','子':'甲','丑':'乙'},
    }
    year_mapping = mapping.get(year_tg)
    if year_mapping is None:
        return None
    return year_mapping.get(month_branch)

# 当前年份干支
def get_current_year_ganzhi():
    current_year = datetime.now().year
    return get_year_tg(current_year), get_year_dz(current_year)

# 生成当前年份的流月干支
def calc_liuyue(year_tg):
    if not year_tg:
        return None
    month_names = ['正月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
    result = []
    for month_name, branch in zip(month_names, dizhi_list):
        stem = get_wuhu_dun_month_tiangan(year_tg, branch)
        if stem is None:
            return None
        result.append((month_name, stem, branch))
    return result

# 生成月限序列
def calc_yuexian(year_tg, tai_sui_dz, birth_year_dz, minggong_dz):
    start_branch = calc_yuexian_start_branch(birth_year_dz, tai_sui_dz, minggong_dz)
    if start_branch is None:
        return None
    month_names = ['正月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
    start_idx = get_dizhi_num(start_branch)
    if start_idx is None:
        return None
    result = []
    for i, month_name in enumerate(month_names):
        branch = dizhi_by_num(start_idx - i)
        stem = get_wuhu_dun_month_tiangan(year_tg, branch)
        if stem is None:
            return None
        result.append((month_name, stem, branch))
    return result


def get_month_num_from_date(year, month, day):
    """根据公历日期，使用最近的中气确定命宫用的月数（寅=1，丑=12）。"""
    from datetime import date

    target = date(year, month, day)
    terms = []
    for current_year in (year - 1, year, year + 1):
        for index, term in enumerate(solarterm.solarterms, start=1):
            terms.append((current_year, index, term(current_year)))

    mid_qi = [(current_year, index, dt) for (current_year, index, dt) in terms if index % 2 == 0]
    mid_qi.sort(key=lambda item: item[2])

    last_mid = None
    for current_year, index, dt in mid_qi:
        if dt <= target:
            last_mid = (current_year, index, dt)
        else:
            break

    if last_mid is None:
        last_mid = mid_qi[-1]

    _, index, _ = last_mid
    month_num = (index // 2) % 12
    if month_num == 0:
        month_num = 12
    return month_num, last_mid


def get_month_dz(year, month, day):
    """按旧规则取月支：过中气进一月。"""
    from datetime import date

    month_num, last_mid = get_month_num_from_date(year, month, day)
    target = date(year, month, day)
    if target > last_mid[2]:
        month_num += 1
    month_num = month_num % 12
    if month_num == 0:
        month_num = 12
    month_dz = month_dz_list[month_num - 1]
    return month_dz, month_num


def get_year_dz(year):
    idx = (year - 4) % 12
    return branch_cycle[idx]


def get_minggong_month_dz_and_num(true_dt):
    method = month_method_var.get() if 'month_method_var' in globals() else ''
    if method == '定气法':
        month_dz, month_num = get_month_dz_from_datetime(true_dt)
        if month_num is None:
            return month_dz, month_num
        # 沿用旧规则：中气后顺延一月
        _, last_mid = get_month_num_from_date(true_dt.year, true_dt.month, true_dt.day)
        if true_dt.date() > last_mid[2]:
            month_num += 1
            if month_num > 12:
                month_num = 1
            month_dz = month_dz_list[month_num - 1]
        return month_dz, month_num
    return get_month_dz(true_dt.year, true_dt.month, true_dt.day)

# 获取年干（简化版，实际需万年历算法）
def get_year_tg(year):
    tg_index = (year - 4) % 10
    return tiangan_list[tg_index]

# 获取时支（简化版，实际需万年历算法）
def get_hour_dz(hour):
    if hour == 23 or hour == 0:
        return '子'
    elif hour == 1 or hour == 2:
        return '丑'
    elif hour == 3 or hour == 4:
        return '寅'
    elif hour == 5 or hour == 6:
        return '卯'
    elif hour == 7 or hour == 8:
        return '辰'
    elif hour == 9 or hour == 10:
        return '巳'
    elif hour == 11 or hour == 12:
        return '午'
    elif hour == 13 or hour == 14:
        return '未'
    elif hour == 15 or hour == 16:
        return '申'
    elif hour == 17 or hour == 18:
        return '酉'
    elif hour == 19 or hour == 20:
        return '戌'
    elif hour == 21 or hour == 22:
        return '亥'
    else:
        return '子'


def parse_pillar(text):
    text = text.replace(' ', '')
    if len(text) == 2:
        return text[0], text[1]
    return None, None

def get_month_tiangan(month_num, year_tg):
    mapping = {
        '甲': ['丙','丁','戊','己','庚','辛','壬','癸','甲','乙','丙','丁'],
        '己': ['丙','丁','戊','己','庚','辛','壬','癸','甲','乙','丙','丁'],
        '乙': ['戊','己','庚','辛','壬','癸','甲','乙','丙','丁','戊','己'],
        '庚': ['戊','己','庚','辛','壬','癸','甲','乙','丙','丁','戊','己'],
        '丙': ['庚','辛','壬','癸','甲','乙','丙','丁','戊','己','庚','辛'],
        '辛': ['庚','辛','壬','癸','甲','乙','丙','丁','戊','己','庚','辛'],
        '丁': ['壬','癸','甲','乙','丙','丁','戊','己','庚','辛','壬','癸'],
        '壬': ['壬','癸','甲','乙','丙','丁','戊','己','庚','辛','壬','癸'],
        '戊': ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸','甲','乙'],
        '癸': ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸','甲','乙'],
    }
    if month_num is None:
        return None
    return mapping.get(year_tg, [None] * 12)[month_num - 1]

from datetime import date as _date

def calc_day_ganzhi(year, month, day):
    try:
        target = _date(year, month, day)
    except Exception:
        return None, None
    ref = _date(1984, 2, 2)  # 常见甲子日参考点
    offset = (target - ref).days
    index = offset % 60
    return tiangan_by_num((index % 10) + 1), branch_cycle[index % 12]

def calc_hour_pillar(day_tg, hour):
    hour_branch = get_hour_dz(hour)
    if day_tg is None or hour_branch is None:
        return None, None
    mapping = {
        '甲': ['丙','丁','戊','己','庚','辛','壬','癸','甲','乙','丙','丁'],
        '己': ['丙','丁','戊','己','庚','辛','壬','癸','甲','乙','丙','丁'],
        '乙': ['戊','己','庚','辛','壬','癸','甲','乙','丙','丁','戊','己'],
        '庚': ['戊','己','庚','辛','壬','癸','甲','乙','丙','丁','戊','己'],
        '丙': ['庚','辛','壬','癸','甲','乙','丙','丁','戊','己','庚','辛'],
        '辛': ['庚','辛','壬','癸','甲','乙','丙','丁','戊','己','庚','辛'],
        '丁': ['壬','癸','甲','乙','丙','丁','戊','己','庚','辛','壬','癸'],
        '壬': ['壬','癸','甲','乙','丙','丁','戊','己','庚','辛','壬','癸'],
        '戊': ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸','甲','乙'],
        '癸': ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸','甲','乙'],
    }
    stems = mapping.get(day_tg)
    if stems is None:
        return None, None
    branch_idx = get_branch_index(hour_branch)
    if branch_idx is None:
        return None, None
    return stems[branch_idx], hour_branch


def update_pillars_from_date():
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        day = int(entry_day.get())
        time_parts = parse_time_text(entry_hour.get())
        if time_parts is None:
            return
        hour, minute = time_parts
    except ValueError:
        return
    calendar_type = var.get()
    if calendar_type == '农历':
        solar = lunar_to_solar(year, month, day)
        if solar is None:
            return
        year, month, day = solar

    birthplace_text = entry_birthplace.get() if 'entry_birthplace' in globals() else ''
    try:
        bazi_info = calc_bazi_pillars_with_true_solar(year, month, day, hour, minute, birthplace_text)
    except (ValueError, RuntimeError):
        return
    year_pillar = bazi_info.get('year_pillar')
    month_pillar = bazi_info.get('month_pillar')
    day_pillar = bazi_info.get('day_pillar')
    hour_pillar = bazi_info.get('hour_pillar')
    # 四柱由当前出生时间、地点和真太阳时唯一决定，必须覆盖旧值，避免跨地点/时间复用旧柱
    try:
        if year_pillar:
            entry_year_pillar.delete(0, tk.END)
            entry_year_pillar.insert(0, year_pillar)
        if month_pillar:
            entry_month_pillar.delete(0, tk.END)
            entry_month_pillar.insert(0, month_pillar)
        if day_pillar:
            entry_day_pillar.delete(0, tk.END)
            entry_day_pillar.insert(0, day_pillar)
        if hour_pillar:
            entry_hour_pillar.delete(0, tk.END)
            entry_hour_pillar.insert(0, hour_pillar)
    except NameError:
        # 如果在调用时相关 Entry 还未创建，则忽略自动填充
        pass
    refresh_dun_display()


def refresh_dun_display():
    """按当前年柱天干刷新日柱/时柱周围的五虎遁提示，不影响四柱本身的取值。"""
    try:
        year_pillar_str = entry_year_pillar.get().strip()
        year_tg = year_pillar_str[0] if year_pillar_str else ''
        if hasattr(entry_day_pillar, 'update_dun'):
            entry_day_pillar.update_dun(year_tg)
        if hasattr(entry_hour_pillar, 'update_dun'):
            entry_hour_pillar.update_dun(year_tg)
    except NameError:
        pass


def force_recalc_pillars():
    """清空四柱输入框后强制按当前输入重算。"""
    try:
        entry_year_pillar.delete(0, tk.END)
        entry_month_pillar.delete(0, tk.END)
        entry_day_pillar.delete(0, tk.END)
        entry_hour_pillar.delete(0, tk.END)
    except NameError:
        return
    update_pillars_from_date()

# 生成男命/女命12宫顺序
palace_names = ['命宫', '财帛宫', '兄弟宫', '田宅宫', '男女宫', '奴仆宫', '妻妾宫', '疾厄宫', '迁移宫', '官禄宫', '福德宫', '相貌宫']

def get_branch_index(dz):
    try:
        return branch_cycle.index(dz)
    except ValueError:
        return None


def generate_palaces(minggong_dz, gender):
    index = get_branch_index(minggong_dz)
    if index is None:
        return None
    step = -1 if gender == '男' else 1
    palaces = []
    current = index
    for _ in range(12):
        palaces.append(branch_cycle[current])
        current = (current + step) % 12
    return palaces

# 农历转阳历
def lunar_to_solar(year, month, day, is_leap=False):
    lunar_date = Lunar(year, month, day, is_leap)
    solar_date = Converter.Lunar2Solar(lunar_date)
    return solar_date.year, solar_date.month, solar_date.day

# 查询命宫
def parse_time_text(time_text):
    if time_text is None:
        return None
    raw = time_text.strip()
    if not raw:
        return None
    minute = 0
    if ':' in raw:
        h, m = raw.split(':', 1)
        h = h.strip()
        m = m.strip()
        if not h:
            return None
        try:
            hour = int(h)
            minute = int(m) if m else 0
        except ValueError:
            return None
    else:
        token = raw.split()[0]
        try:
            hour = int(token)
        except ValueError:
            return None
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return None
    return hour, minute


def parse_hour_text(hour_text):
    parts = parse_time_text(hour_text)
    if parts is None:
        return None
    return parts[0]


month_names = ['正月','二月','三月','四月','五月','六月','七月','八月','九月','十月','冬月','腊月']

def format_summary_lines(lines, per_line=3, sep='    '):
    """将多条摘要字段按 per_line 个合并为一行，减少纵向占用高度。"""
    grouped = [sep.join(lines[i:i + per_line]) for i in range(0, len(lines), per_line)]
    return '\n'.join(grouped)


class PillarEntry:
    """天干/地支纵向两行展示的输入框；对外暴露 get/delete/insert，与 tk.Entry 用法保持一致，不改变取值逻辑。"""

    def __init__(self, parent, width=3):
        self.frame = tk.Frame(parent, bd=1, relief='solid')
        self.tg_var = tk.StringVar()
        self.dz_var = tk.StringVar()
        self.tg_entry = tk.Entry(self.frame, width=width, textvariable=self.tg_var, justify='center',
                                  fg='#8B0000', bd=0, highlightthickness=0)
        self.dz_entry = tk.Entry(self.frame, width=width, textvariable=self.dz_var, justify='center',
                                  fg='#00008B', bd=0, highlightthickness=0)
        self.tg_entry.grid(row=0, column=0)
        self.dz_entry.grid(row=1, column=0)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def get(self):
        return (self.tg_var.get() + self.dz_var.get()).strip()

    def delete(self, start, end):
        self.tg_var.set('')
        self.dz_var.set('')

    def insert(self, index, text):
        text = (text or '').strip()
        self.tg_var.set(text[0] if len(text) >= 1 else '')
        self.dz_var.set(text[1] if len(text) >= 2 else '')


class DunPillarEntry:
    """在天干地支两行展示的基础上，围绕柱位上下追加五虎遁的"遁干/遁支"提示；
    对外接口仍与 tk.Entry 一致（get/delete/insert），不影响原有取值逻辑。"""

    def __init__(self, parent, width=3):
        self.outer = tk.Frame(parent)
        self.dun_gan_label = tk.Label(self.outer, text='', font=('TkDefaultFont', 8), fg='#555555')
        self.dun_gan_label.pack()
        self.pillar = PillarEntry(self.outer, width=width)
        self.pillar.frame.pack()
        self.dun_zhi_label = tk.Label(self.outer, text='', font=('TkDefaultFont', 8), fg='#555555')
        self.dun_zhi_label.pack()

    def grid(self, **kwargs):
        self.outer.grid(**kwargs)

    def get(self):
        return self.pillar.get()

    def delete(self, start, end):
        self.pillar.delete(start, end)

    def insert(self, index, text):
        self.pillar.insert(index, text)

    def update_dun(self, year_tg):
        """按年干用五虎遁计算：遁支=柱地支正向查表得天干；遁干=柱天干反向查表得地支（可能有两个）。"""
        pillar_str = self.get()
        if not year_tg or len(pillar_str) < 2:
            self.dun_gan_label.config(text='')
            self.dun_zhi_label.config(text='')
            return
        stem, branch = pillar_str[0], pillar_str[1]
        zhi_stem = get_wuhu_dun_month_tiangan(year_tg, branch)
        dun_zhi_text = f'{zhi_stem}{branch}' if zhi_stem else ''
        gan_branches = [b for b in dizhi_list if get_wuhu_dun_month_tiangan(year_tg, b) == stem]
        dun_gan_text = ' '.join(f'{stem}{b}' for b in gan_branches)
        self.dun_gan_label.config(text=dun_gan_text)
        self.dun_zhi_label.config(text=dun_zhi_text)


def clear_result_table():
    for item in result_table.get_children():
        result_table.delete(item)


def display_result(title, content):
    result_title_label.config(text=title)
    result_info_label.config(text=content)
    clear_result_table()
    show_result_page()


def display_result_table(title, summary, rows):
    result_title_label.config(text=title)
    result_info_label.config(text=summary)
    clear_result_table()
    for label, row in rows:
        result_table.insert('', 'end', values=[label] + row)
    show_result_page()


def show_input_page():
    result_page.pack_forget()
    input_page.pack(fill='both', expand=True)


def show_result_page():
    input_page.pack_forget()
    result_page.pack(fill='both', expand=True)


def render_standard_dayun_table(table, dayun_rows, expand_all=True):
    """将既有普通排盘数据按目标界面渲染为逐步大运表，不参与计算。
    两层结构：大运（父行）→ 流年（子行）；流月不再作为孙行，改由独立的横向流月条展示。
    expand_all=True 时默认展开大运层，使全部流年行直接可见。
    """
    columns = ('序号', '大运', '起始年龄', '结束年龄', '起始年份', '结束年份')
    table.configure(columns=columns, show='tree headings')
    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=108 if column != '大运' else 88, anchor='center')
    # 展开树形结构需要为层级指示留出空间
    table.column('#0', width=150, minwidth=60, stretch=False)
    table.heading('#0', text='')

    # 彩色层级：大运（浅蓝），流年（白色）
    table.tag_configure('dayun', background='#E8F0FE')
    table.tag_configure('flow_year', background='#FFFFFF')

    for row in dayun_rows:
        # 大运父行
        dayun_iid = f"dy_{row['index']}"
        table.insert('', 'end', iid=dayun_iid, values=(
            row['index'], row['ganzhi'], row['start_age'], row['end_age'],
            row['start_year'], row['end_year'],
        ), tags=('dayun',))

        # 流年子行：每步大运覆盖的年份逐一展开（流月由横向流月条按选中流年切换）
        for year in range(row['start_year'], row['end_year'] + 1):
            flow_ganzhi = get_year_tg(year) + get_year_dz(year)
            flow_iid = f"dy_{row['index']}_y{year}"
            table.insert(dayun_iid, 'end', iid=flow_iid, values=(
                '', '', '', '',
                year, flow_ganzhi,
            ), tags=('flow_year',))

    if expand_all:
        # 默认展开大运层，使全部流年行可见
        for dayun_iid in table.get_children(''):
            table.item(dayun_iid, open=True)


def format_dayun_step_text(row):
    """把一步大运转为步骤头文本（大运位于该步流年上方）。"""
    return f"大运   {row['ganzhi']}\n{row['start_year']}\n{row['start_age']}岁"


def find_dayun_block(dayun_rows, year):
    """返回覆盖给定年份的大运行（按起始/结束年份查找），找不到返回 None。"""
    for row in dayun_rows:
        s, e = row.get('start_year'), row.get('end_year')
        if s is not None and e is not None and s <= year <= e:
            return row
    return None


def create_flow_month_strip(parent):
    """流月条（含步骤头）：上为“大运”行，其下为“流年”行，再下为 正月~十二月 12 个流月小格。
    返回 (frame, update_fn, cells)；update_fn(year) 填入该年份的 12 个流月并刷新“流年”行；
    update_fn.set_step(dayun_text) 刷新“大运”行（位于流年上方）。"""
    month_names = ['正月', '二月', '三月', '四月', '五月', '六月',
                   '七月', '八月', '九月', '十月', '十一月', '十二月']
    frame = tk.Frame(parent)
    # 大运行：该步大运（列示在流年上方）
    dayun_label = tk.Label(frame, text='', anchor='w', fg='#1F4E79',
                           font=('TkDefaultFont', 10, 'bold'))
    dayun_label.pack(fill='x', padx=(0, 4))
    # 流年行：该步流年（在大运下方）
    flowyear_label = tk.Label(frame, text='', anchor='w', fg='#8B4513',
                              font=('TkDefaultFont', 10, 'bold'))
    flowyear_label.pack(fill='x', padx=(0, 4))
    # 流月小格横排行（在流年下方）
    month_row = tk.Frame(frame)
    month_row.pack(fill='x', padx=(0, 4))
    tk.Label(month_row, text=f"{rt('row_flow_month')}：", fg='#333333').pack(
        side='left', padx=(0, 4))
    cells = []
    for month_name in month_names:
        cell = tk.Frame(month_row, bd=1, relief='ridge', padx=4, pady=1)
        tk.Label(cell, text=month_name, font=('TkDefaultFont', 9), fg='#555555').pack()
        gz_lbl = tk.Label(cell, text='', font=('TkDefaultFont', 10, 'bold'), fg='#8B0000')
        gz_lbl.pack()
        cell.pack(side='left', padx=1)
        cells.append((month_name, gz_lbl))

    def update_fn(year):
        liuyue = calc_liuyue(get_year_tg(year))
        if liuyue is None:
            for _, gz_lbl in cells:
                gz_lbl.config(text='')
            return
        for (_, gz_lbl), (_, stem, branch) in zip(cells, liuyue):
            gz_lbl.config(text=f'{stem}{branch}')
        flowyear_label.config(
            text=f"{rt('summary_flow_year')}：{year} {get_year_tg(year)}{get_year_dz(year)}")

    def set_step(dayun_text):
        dayun_label.config(text=dayun_text)

    update_fn.set_step = set_step
    return frame, update_fn, cells


def bind_flow_month_strip_update(table, update_fn):
    """绑定 Treeview 选中事件：选中流年行 → 切换横向流月条并更新步骤头（大运在流年上方）；
    选中大运行则保持流月不变。"""
    def on_select(event):
        selected = table.selection()
        if not selected:
            return
        iid = selected[0]
        if '_y' not in iid:
            return
        year_text = iid.rsplit('_y', 1)[1]
        if not year_text.isdigit():
            return
        update_fn(int(year_text))
        # 步骤头：从父行（大运）读取该步大运，列示在流年上方
        step_fn = getattr(update_fn, 'set_step', None)
        if step_fn is None:
            return
        parent_iid = table.parent(iid) if table.exists(iid) else ''
        if not parent_iid or not table.exists(parent_iid):
            return
        vals = table.item(parent_iid, 'values')
        if len(vals) >= 6:
            step_row = {
                'ganzhi': vals[1], 'start_age': vals[2], 'end_age': vals[3],
                'start_year': vals[4], 'end_year': vals[5],
            }
            step_fn(format_dayun_step_text(step_row))

    table.bind('<<TreeviewSelect>>', on_select)
    return on_select


class DayunFlowGrid(tk.Frame):
    """参照图（image6/image9）的大运密集网格（表二布局）：
    顶行“大运：干支链” + 每步大运一列：块头（起运岁/起运年份/大运干支） + 10 个流年格纵向堆叠，
    多步大运并列成列。每个流年格 = 流年年份（灰） + 流年干支（加粗），单行紧凑放置，
    10 格全部可见；按需求不再显示格内十神简写。
    点击流年格 → on_year_select(year, block_row) 联动下方横向流月条。
    """

    HEADER_BG = '#DEEBF7'
    CHAIN_BG = '#E8F0FE'
    SELECT_BG = '#FFF2CC'

    def __init__(self, parent, on_year_select=None):
        super().__init__(parent)
        self.on_year_select = on_year_select
        self.year_cells = {}      # year -> {'frame','year_lbl','gz'}
        self.year_block = {}      # year -> 大运行(dict)
        self.selected_year = None
        canvas_holder = tk.Frame(self)
        canvas_holder.pack(fill='both', expand=True)
        self.canvas = tk.Canvas(canvas_holder, highlightthickness=0, bg='#FFFFFF')
        vsb = ttk.Scrollbar(canvas_holder, orient='vertical', command=self.canvas.yview)
        hsb = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        hsb.pack(side='bottom', fill='x')
        vsb.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.body = tk.Frame(self.canvas, bg='#FFFFFF')
        self._win = self.canvas.create_window((0, 0), window=self.body, anchor='nw')
        self.body.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

    def render(self, dayun_rows, default_year=None):
        for child in self.body.winfo_children():
            child.destroy()
        self.year_cells = {}
        self.year_block = {}
        self.selected_year = default_year
        if not dayun_rows:
            return
        body = self.body
        chain = '  '.join((row.get('ganzhi') or '') for row in dayun_rows)
        tk.Label(body, text=f'大运：{chain}', anchor='w', font=('TkDefaultFont', 9, 'bold'),
                 fg='#1F4E79', bg=self.CHAIN_BG).grid(
                     row=0, column=0, columnspan=len(dayun_rows), sticky='ew',
                     padx=2, pady=(0, 1), ipady=1)
        for c, row in enumerate(dayun_rows):
            band = tk.Frame(body, bg='#FFFFFF')
            band.grid(row=1, column=c, sticky='n', padx=2, pady=1)
            self._build_header(band, row)
            start_year = int(row.get('start_year') or 0)
            end_year = int(row.get('end_year') or (start_year + 9))
            for year in range(start_year, end_year + 1):
                gz = get_year_tg(year) + get_year_dz(year)
                info = self._build_year_cell(band, year, gz)
                self.year_cells[year] = info
                self.year_block[year] = row
        self._refresh_selection()

    def _build_header(self, parent, row):
        frame = tk.Frame(parent, bg=self.HEADER_BG, bd=1, relief='ridge')
        tk.Label(frame, text=f"{row.get('start_age') or '?'}岁", font=('TkDefaultFont', 8),
                 fg='#404040', bg=self.HEADER_BG).pack()
        tk.Label(frame, text=str(row.get('start_year') or '?'), font=('TkDefaultFont', 8),
                 fg='#404040', bg=self.HEADER_BG).pack()
        tk.Label(frame, text=row.get('ganzhi') or '', font=('TkDefaultFont', 9, 'bold'),
                 fg='#1F4E79', bg=self.HEADER_BG, width=5).pack()
        frame.pack(pady=(0, 1))

    def _build_year_cell(self, parent, year, ganzhi):
        """每个流年格 = 流年年份（灰） + 流年干支（加粗），单行紧凑放置。
        原格内“天干十神/地支本气十神”简写块已按需求移除，改用流年年份；
        10 格单行堆叠，全部可见。"""
        cell = tk.Frame(parent, bd=1, relief='ridge', bg='#FFFFFF')
        year_lbl = tk.Label(cell, text=str(year), font=('TkDefaultFont', 8),
                            fg='#8A8A8A', bg='#FFFFFF')
        year_lbl.pack(side='left', padx=(3, 0))
        gz_lbl = tk.Label(cell, text=ganzhi, font=('TkDefaultFont', 8, 'bold'),
                          fg='#333333', bg='#FFFFFF')
        gz_lbl.pack(side='left', padx=(0, 3))
        for widget in (cell, year_lbl, gz_lbl):
            widget.bind('<Button-1>', lambda e, y=year: self._select_year(y))
        cell.pack(pady=0)
        return {'frame': cell, 'year_lbl': year_lbl, 'gz': gz_lbl}

    def _select_year(self, year):
        if year not in self.year_cells or year not in self.year_block:
            return
        self.selected_year = year
        self._refresh_selection()
        if self.on_year_select is not None:
            self.on_year_select(year, self.year_block[year])

    def _refresh_selection(self):
        for year, info in self.year_cells.items():
            bg = self.SELECT_BG if year == self.selected_year else '#FFFFFF'
            info['frame'].config(bg=bg)
            info['gz'].config(bg=bg)
            info['year_lbl'].config(bg=bg)


def query_ordinary():
    """展示现有普通排盘（大运）计算结果，不改变计算逻辑。"""
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        day = int(entry_day.get())
        time_parts = parse_time_text(entry_hour.get())
        if time_parts is None:
            raise ValueError
        hour, minute = time_parts
    except ValueError:
        messagebox.showerror(rt('err_title'), rt('err_invalid_datetime'))
        return

    if var.get() == '农历':
        solar = lunar_to_solar(year, month, day)
        if solar is None:
            messagebox.showerror(rt('err_title'), rt('err_invalid_lunar'))
            return
        year, month, day = solar

    birthplace_text = entry_birthplace.get() if 'entry_birthplace' in globals() else ''
    solar_ctx = build_true_solar_context(
        year, month, day, hour, minute, birthplace_text,
        summer_time_var.get() if 'summer_time_var' in globals() else None,
    )
    if not solar_ctx['used_true_solar']:
        messagebox.showerror(rt('err_title'), '出生地未解析，无法使用真太阳时排盘')
        return

    gender = gender_var.get()
    result = calc_dayun_standard(solar_ctx['true_dt'], gender, sect=2, count=10)
    if result is None:
        messagebox.showerror(rt('err_title'), '普通排盘计算库不可用')
        return

    bazi = calc_bazi_pillars_with_true_solar(
        year, month, day, hour, minute, birthplace_text,
        summer_time_var.get() if 'summer_time_var' in globals() else None,
    )
    summary_lines = [
        f"普通排盘：{'顺排' if result['forward'] else '逆排'}",
        f"八字：{bazi['year_pillar']} {bazi['month_pillar']} {bazi['day_pillar']} {bazi['hour_pillar']}",
        f"标准时：{solar_ctx['input_dt'].strftime('%Y-%m-%d %H:%M')}    出生地：{solar_ctx['place_name']}",
        f"真太阳时修正量：{format_offset_hhmm(solar_ctx['offset_minutes'])}    修正后时间：{solar_ctx['true_dt'].strftime('%Y-%m-%d %H:%M')}",
        f"早晚子时：{solar_ctx['zi_hour_type'] or '非子时'}",
        f"起运：出生后{result['start_year']}年{result['start_month']}月{result['start_day']}天{result['start_hour']}小时    {'顺排' if result['forward'] else '逆排'}",
    ]
    result_ordinary_title_label.config(text='普通排盘')
    result_ordinary_info_label.config(text='\n'.join(summary_lines), justify='left')
    # 密集网格渲染（参照图）：大运块头 + 流年干支；格内显示流年年份（不再显示十神）
    ordinary_flow_grid.render(result['dayun'], default_year=datetime.now().year)
    # 默认未选中流年时：横向流月条显示“当下时间年份”的 12 个流月，并显示该年所属大运步骤头（大运在流年上方）
    if hasattr(ordinary_flow_month_update, 'set_step'):
        step = find_dayun_block(result['dayun'], datetime.now().year)
        if step is None:
            step = result['dayun'][0]
        ordinary_flow_month_update.set_step(format_dayun_step_text(step))
    ordinary_flow_month_update(datetime.now().year)
    result_notebook.select(ordinary_result_frame)


def start_chart_query():
    """完成输入后进入结果页，并先展示基本命盘。"""
    query_minggong()
    query_yuexian()


def on_result_tab_changed(_event=None):
    if result_notebook.tab(result_notebook.select(), 'text') == '普通排盘':
        query_ordinary()


def query_luming():
    """根据禄命页签的人工选项生成独立禄命大运结果。"""
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        day = int(entry_day.get())
        time_parts = parse_time_text(entry_hour.get())
        if time_parts is None:
            raise ValueError
        hour, minute = time_parts
    except ValueError:
        messagebox.showerror(rt('err_title'), rt('err_invalid_datetime'))
        return

    if var.get() == '农历':
        solar = lunar_to_solar(year, month, day)
        if solar is None:
            messagebox.showerror(rt('err_title'), rt('err_invalid_lunar'))
            return
        year, month, day = solar

    birthplace_text = entry_birthplace.get() if 'entry_birthplace' in globals() else ''
    summer_enabled = summer_time_var.get() if 'summer_time_var' in globals() else None
    solar_ctx = build_true_solar_context(year, month, day, hour, minute, birthplace_text, summer_enabled)
    if not solar_ctx['used_true_solar']:
        messagebox.showerror(rt('err_title'), '出生地未解析，无法使用真太阳时排盘')
        return

    try:
        bazi = calc_bazi_pillars_with_true_solar(
            year, month, day, hour, minute, birthplace_text, summer_enabled
        )
        solar = LunarPythonSolar.fromYmdHms(
            solar_ctx['true_dt'].year, solar_ctx['true_dt'].month,
            solar_ctx['true_dt'].day, solar_ctx['true_dt'].hour,
            solar_ctx['true_dt'].minute, solar_ctx['true_dt'].second,
        )
        lunar = solar.getLunar()
        previous_jie = _solar_to_datetime(lunar.getPrevJieQi().getSolar())
        next_jie = _solar_to_datetime(lunar.getNextJieQi().getSolar())
        options = luming_rules.build_luming_options(
            luming_base_var.get().replace('排盘', ''),
            luming_taiji_var.get(),
            luming_dayun_var.get().replace('排大运', ''),
            luming_direction_var.get().replace('大运', ''),
        )
        qiyun = luming_rules.calculate_qiyun(
            solar_ctx['true_dt'], previous_jie, next_jie,
            bazi['year_pillar'][0], gender_var.get(), precision='minute',
        )
        pillars = {
            '年柱': bazi['year_pillar'], '月柱': bazi['month_pillar'],
            '日柱': bazi['day_pillar'], '时柱': bazi['hour_pillar'],
        }
        dayun = luming_rules.generate_luming_dayun(pillars, options, qiyun)
    except (AttributeError, IndexError, TypeError, ValueError, RuntimeError) as exc:
        messagebox.showerror(rt('err_title'), f'禄命排盘计算失败：{exc}')
        return

    result = {'pillars': pillars, 'qiyun': qiyun, 'dayun': dayun}
    snapshot = luming_rules.build_snapshot(
        {'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute,
         'gender': gender_var.get(), 'birthplace': birthplace_text},
        {key: str(value) for key, value in solar_ctx.items()},
        {'options': options, **result},
    )
    snapshot_path = os.path.join(
        os.path.dirname(__file__), 'output', 'luming_snapshots',
        f'luming_{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}.json',
    )
    luming_rules.save_snapshot(snapshot, snapshot_path)
    luming_result_info_label.config(
        text=(f"八字：{' '.join(pillars.values())}\n"
              f"早晚子时：{solar_ctx.get('zi_hour_type') or '非子时'}\n"
              f"起运：{qiyun['age_text']}（{qiyun['direction']}，方案{qiyun['scheme']}）\n"
              f"起运时间：{qiyun['start_datetime']}\n"
              f"立极点：{options['taiji_point']}    大运取柱：{options['dayun_pillar']}    大运方向：{options['direction']}\n"
              f"快照版本：{snapshot['ruleVersion']} / {snapshot['baseVersion']}\n"
              f"快照文件：{snapshot_path}"),
        justify='left',
    )
    # 补齐整数字段后按参照图密集网格渲染（大运块头 + 流年干支/十神）。
    # 禄命采用 10 年/运（同普通排盘与参照图）：起运年龄/年份 +10n，结束=起始+9。
    qiyun_start_year = qiyun['start_datetime'].year
    qiyun_start_age = int(qiyun['years'])
    for row in dayun:
        row['start_age'] = qiyun_start_age + (row['index'] - 1) * 10
        row['end_age'] = row['start_age'] + 9
        row['start_year'] = qiyun_start_year + (row['index'] - 1) * 10
        row['end_year'] = row['start_year'] + 9
    # 格内不再显示十神：网格渲染只需大运块头 + 流年干支 + 流年年份
    luming_flow_grid.render(dayun, default_year=datetime.now().year)
    # 默认未选中流年时：横向流月条显示“当下时间年份”的 12 个流月，并显示该年所属大运步骤头（大运在流年上方）
    if hasattr(luming_flow_month_update, 'set_step'):
        step = find_dayun_block(dayun, datetime.now().year)
        if step is None:
            step = dayun[0]
        luming_flow_month_update.set_step(format_dayun_step_text(step))
    luming_flow_month_update(datetime.now().year)
    result_notebook.select(luming_result_frame)


def query_minggong():
    if 'month_method_var' in globals() and month_method_var.get() not in ('平气法', '定气法'):
        messagebox.showerror(rt('err_title'), rt('err_choose_month_method'))
        return
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        day = int(entry_day.get())
        time_parts = parse_time_text(entry_hour.get())
        if time_parts is None:
            raise ValueError
        hour, minute = time_parts
    except ValueError:
        messagebox.showerror(rt('err_title'), rt('err_invalid_datetime'))
        return
    update_pillars_from_date()
    calendar_type = var.get()
    if calendar_type == '农历':
        solar = lunar_to_solar(year, month, day)
        if solar is None:
            messagebox.showerror(rt('err_title'), rt('err_invalid_lunar'))
            return
        year, month, day = solar

    birthplace_text = entry_birthplace.get() if 'entry_birthplace' in globals() else ''
    solar_ctx = build_true_solar_context(
        year, month, day, hour, minute, birthplace_text,
        summer_time_var.get() if 'summer_time_var' in globals() else None,
    )
    if not solar_ctx['used_true_solar']:
        messagebox.showerror(rt('err_title'), '出生地未解析，无法使用真太阳时排盘')
        return
    input_dt = solar_ctx['input_dt']
    true_dt = solar_ctx['true_dt']
    offset_minutes = solar_ctx['offset_minutes']
    used_true_solar = solar_ctx['used_true_solar']
    longitude = solar_ctx['longitude']
    latitude = solar_ctx['latitude']
    place_name = solar_ctx['place_name']

    year_tg = get_year_tg(true_dt.year)
    hour_dz = get_hour_dz(true_dt.hour)

    month_dz, month_num = get_minggong_month_dz_and_num(true_dt)
    month_line = f"{rt('month_line')}：{month_dz}"

    mg_dz = calc_minggong_dizhi(month_num, hour_dz)
    specified_minggong = entry_specified_minggong.get().strip()
    if specified_minggong:
        mg_dz = specified_minggong
    else:
        mg_dz = calc_minggong_dizhi(month_num, hour_dz)
        if mg_dz:
            entry_specified_minggong.delete(0, tk.END)
            entry_specified_minggong.insert(0, mg_dz)

    if mg_dz is None:
        messagebox.showerror(rt('err_title'), rt('err_hour_branch'))
        return
    mg_tg = calc_minggong_tiangan(year_tg, mg_dz)
    if mg_tg is None:
        messagebox.showerror(rt('err_title'), rt('err_year_stem'))
        return
    gender = gender_var.get()
    palaces = generate_palaces(mg_dz, gender)
    if palaces is None:
        messagebox.showerror(rt('err_title'), rt('err_minggong_invalid'))
        return
    palace_lines = '\n'.join(
        f'{i + 1}{palace_names[i]}：{palaces[i]}'
        for i in range(12)
    )
    calendar_str = rt('calendar_lunar') if calendar_type == '农历' else rt('calendar_solar')
    solar_debug_lines = [
        f"{rt('summary_standard_time')}：{input_dt.strftime('%Y-%m-%d %H:%M')}",
    ]
    if used_true_solar:
        if place_name:
            solar_debug_lines.append(f"{rt('summary_birthplace')}：{place_name}")
        if latitude is not None:
            solar_debug_lines.append(f"{rt('summary_coords')}：{latitude:.4f}N {longitude:.4f}E")
        else:
            solar_debug_lines.append(f"{rt('summary_longitude')}：{longitude:.4f}°E")
        solar_debug_lines.append(f"{rt('summary_true_solar_offset')}：{format_offset_hhmm(offset_minutes)}")
        solar_debug_lines.append(f"{rt('summary_true_time')}：{true_dt.strftime('%Y-%m-%d %H:%M')}")
    else:
        solar_debug_lines.append(f"{rt('summary_true_solar_offset')}：{rt('summary_true_solar_disabled')}")
        solar_debug_lines.append(f"{rt('summary_true_time')}：{true_dt.strftime('%Y-%m-%d %H:%M')}")
    solar_debug_lines.append(f"{rt('summary_final_hour')}：{hour_dz}")

    extra_info_lines = build_zhiyi_extra_info(input_dt, true_dt, gender, birthplace_text, month_method_var.get() if 'month_method_var' in globals() else '定气法')
    head_lines = [f"{rt('summary_minggong')}：{mg_dz}", f"{rt('year_stem')}：{year_tg}", month_line, f"{rt('hour_branch')}：{hour_dz}"]
    solar_info_block = format_summary_lines(head_lines + solar_debug_lines) + '\n'
    extra_info_block = (format_summary_lines(extra_info_lines) + '\n') if extra_info_lines else ''
    result = (
        f'{solar_info_block}'
        f'{extra_info_block}'
        f"({rt('result_input_hint').format(calendar=calendar_str)})\n\n"
        f'{palace_lines}'
    )
    display_result(rt('result_title_minggong'), result)


def query_yuexian():
    if 'month_method_var' in globals() and month_method_var.get() not in ('平气法', '定气法'):
        messagebox.showerror(rt('err_title'), rt('err_choose_month_method'))
        return
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        day = int(entry_day.get())
        time_parts = parse_time_text(entry_hour.get())
        if time_parts is None:
            raise ValueError
        hour, minute = time_parts
    except ValueError:
        messagebox.showerror(rt('err_title'), rt('err_invalid_datetime'))
        return

    update_pillars_from_date()
    calendar_type = var.get()
    if calendar_type == '农历':
        solar = lunar_to_solar(year, month, day)
        if solar is None:
            messagebox.showerror(rt('err_title'), rt('err_invalid_lunar'))
            return
        year, month, day = solar

    birthplace_text = entry_birthplace.get() if 'entry_birthplace' in globals() else ''
    solar_ctx = build_true_solar_context(
        year, month, day, hour, minute, birthplace_text,
        summer_time_var.get() if 'summer_time_var' in globals() else None,
    )
    if not solar_ctx['used_true_solar']:
        messagebox.showerror(rt('err_title'), '出生地未解析，无法使用真太阳时排盘')
        return
    input_dt = solar_ctx['input_dt']
    true_dt = solar_ctx['true_dt']
    offset_minutes = solar_ctx['offset_minutes']
    used_true_solar = solar_ctx['used_true_solar']
    longitude = solar_ctx['longitude']
    latitude = solar_ctx['latitude']
    place_name = solar_ctx['place_name']

    birth_year_tg = get_year_tg(true_dt.year)
    birth_year_dz = get_year_dz(true_dt.year)

    year_pillar = entry_year_pillar.get().strip()
    month_pillar = entry_month_pillar.get().strip()
    day_pillar = entry_day_pillar.get().strip()
    hour_pillar = entry_hour_pillar.get().strip()
    month_dz, month_num = get_minggong_month_dz_and_num(true_dt)

    user_year_tg, user_year_dz = parse_pillar(year_pillar)
    if user_year_tg and user_year_dz:
        benming_year_tg, benming_year_dz = user_year_tg, user_year_dz
    else:
        benming_year_tg, benming_year_dz = birth_year_tg, birth_year_dz

    user_hour_tg, user_hour_dz = parse_pillar(hour_pillar)
    if user_hour_dz:
        hour_dz = user_hour_dz
    else:
        hour_dz = get_hour_dz(true_dt.hour)
    if hour_dz is None:
        messagebox.showerror(rt('err_title'), rt('err_hour_text'))
        return

    specified_minggong = entry_specified_minggong.get().strip()
    if specified_minggong:
        mg_dz = specified_minggong
    else:
        mg_dz = calc_minggong_dizhi(month_num, hour_dz)
        if mg_dz:
            entry_specified_minggong.delete(0, tk.END)
            entry_specified_minggong.insert(0, mg_dz)

    mg_tg = calc_minggong_tiangan(birth_year_tg, mg_dz) if mg_dz else None
    if mg_dz is None or mg_tg is None:
        messagebox.showerror(rt('err_title'), rt('err_minggong_calc'))
        return

    gender = gender_var.get()
    palaces = generate_palaces(mg_dz, gender)
    if palaces is None:
        messagebox.showerror(rt('err_title'), rt('err_minggong_invalid'))
        return

    flow_year_text = entry_flow_year.get().strip()
    if not flow_year_text:
        flow_year = datetime.now().year
    else:
        try:
            flow_year = int(flow_year_text)
        except ValueError:
            messagebox.showerror(rt('err_title'), rt('err_flow_year_number'))
            return

    flow_year_tg = get_year_tg(flow_year)
    flow_year_dz = get_year_dz(flow_year)

    flow_suqian = calc_suqian_12shen(flow_year_dz)
    flow_maqian = calc_maqian_12shen_for_year_branch(flow_year_dz)
    flow_boshi = calc_boshi_12shen(flow_year_tg)
    if flow_suqian is None or flow_maqian is None or flow_boshi is None:
        messagebox.showerror(rt('err_title'), rt('err_flow_year_invalid'))
        return

    rows = []
    yuexian_branches = []

    liuyue = calc_liuyue(flow_year_tg)
    if liuyue is None:
        messagebox.showerror(rt('err_title'), rt('err_flow_month_invalid'))
        return
    liuyue_branches = [dz for _, _, dz in liuyue]
    rows.append((rt('row_flow_month'), [f'{tg}{dz}' for _, tg, dz in liuyue]))

    if benming_year_dz and mg_dz:
        start_branch = calc_yuexian_start_branch(benming_year_dz, flow_year_dz, mg_dz)
        if start_branch is None:
            messagebox.showerror(rt('err_title'), rt('err_ganzhi_invalid_calc_yuexian'))
            return
        yuexian = calc_yuexian(flow_year_tg, flow_year_dz, benming_year_dz, mg_dz)
        if yuexian is None:
            messagebox.showerror(rt('err_title'), rt('err_ganzhi_invalid_calc_yuexian'))
            return
        yuexian_branches = [dz for _, _, dz in yuexian]
        rows.append((rt('row_yuexian'), [f'{tg}{dz}' for _, tg, dz in yuexian]))

        palace_map = {branch: palace_names[i] for i, branch in enumerate(palaces)}
        rows.append((rt('row_flow_12gong'), [palace_map.get(dz, '') for dz in liuyue_branches]))
        rows.append((rt('row_benming_12gong'), [palace_map.get(dz, '') for dz in yuexian_branches]))

    benming_suqian = calc_suqian_12shen(benming_year_dz)
    benming_maqian = calc_maqian_12shen_for_year_branch(benming_year_dz)
    benming_boshi = calc_boshi_12shen(benming_year_tg)
    if benming_suqian is None or benming_maqian is None or benming_boshi is None:
        messagebox.showerror(rt('err_title'), rt('err_benming_invalid'))
        return
    benming_suqian_map = {branch: shen for branch, shen in benming_suqian}
    benming_maqian_map = {branch: shen for branch, shen, stage in benming_maqian}
    benming_boshi_map = {branch: shen for branch, shen in benming_boshi}
    rows.append((rt('row_benming_suqian'), [benming_suqian_map.get(dz, '') for dz in yuexian_branches]))
    rows.append((rt('row_benming_maqian'), [benming_maqian_map.get(dz, '') for dz in yuexian_branches]))
    rows.append((rt('row_benming_boshi'), [benming_boshi_map.get(dz, '') for dz in yuexian_branches]))

    flow_suqian_map = {branch: shen for branch, shen in flow_suqian}
    flow_boshi_map = {branch: shen for branch, shen in flow_boshi}
    flow_maqian_map = {branch: shen for branch, shen, stage in flow_maqian}
    rows.append((rt('row_flow_suqian'), [flow_suqian_map.get(dz, '') for dz in yuexian_branches]))
    rows.append((rt('row_flow_boshi'), [flow_boshi_map.get(dz, '') for dz in yuexian_branches]))
    rows.append((rt('row_flow_maqian'), [flow_maqian_map.get(dz, '') for dz in yuexian_branches]))

    year_label = year_pillar if year_pillar else f'{birth_year_tg}{birth_year_dz}'
    month_label = month_pillar if month_pillar else f'?{month_dz}'
    day_label = day_pillar if day_pillar else '未输入'
    hour_label = hour_pillar if hour_pillar else f'?{hour_dz}'

    summary_lines = [
        f"{rt('summary_flow_year')}：{flow_year} {flow_year_tg}{flow_year_dz}",
        f"{rt('summary_minggong')}：{mg_dz}",
        f"{rt('summary_bazi')}：{year_label} {month_label} {day_label} {hour_label}",
        f"{rt('summary_standard_time')}：{input_dt.strftime('%Y-%m-%d %H:%M')}",
    ]
    if used_true_solar:
        if place_name:
            summary_lines.append(f"{rt('summary_birthplace')}：{place_name}")
        if latitude is not None:
            summary_lines.append(f"{rt('summary_coords')}：{latitude:.4f}N {longitude:.4f}E")
        else:
            summary_lines.append(f"{rt('summary_longitude')}：{longitude:.4f}°E")
        summary_lines.append(f"{rt('summary_true_solar_offset')}：{format_offset_hhmm(offset_minutes)}")
    else:
        summary_lines.append(f"{rt('summary_true_solar_offset')}：{rt('summary_true_solar_disabled')}")
    summary_lines.append(f"{rt('summary_true_time')}：{true_dt.strftime('%Y-%m-%d %H:%M')}")
    summary_lines.append(f"{rt('summary_final_hour')}：{hour_dz}")
    if benming_year_tg and benming_year_dz:
        summary_lines.append(f"{rt('summary_benming_year')}：{benming_year_tg}{benming_year_dz}")

    extra_info_lines = build_zhiyi_extra_info(input_dt, true_dt, gender, birthplace_text, month_method_var.get() if 'month_method_var' in globals() else '定气法')
    if extra_info_lines:
        summary_lines.extend(extra_info_lines)
    summary = format_summary_lines(summary_lines)
    display_result_table(rt('result_title_bazi'), summary, rows)

root = tk.Tk()
root.title(t('app_title'))
# 结果表格含13列（项目+12月），默认按内容自适应可能超出屏幕宽度，启动时最大化窗口以完整显示
try:
    root.state('zoomed')
except tk.TclError:
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

input_page = tk.Frame(root)
result_page = tk.Frame(root)
input_page.pack(fill='both', expand=True)

frame = tk.Frame(input_page)
frame.pack(padx=12, pady=20, anchor='w')

# 顶部“类型 / 性别 / 语言”行放入独立子容器（占用 col0-13 整行）：其较宽控件不再撑大外层网格
# 的共享列宽，使下方的日期行（含右侧 出生地/平气法·定气法）在较窄屏幕上也能完整横向显示。
top_group = tk.Frame(frame)
top_group.grid(row=0, column=0, columnspan=14, sticky='w')

var = tk.StringVar(value='阳历')
var.trace_add('write', refresh_summer_time_suggestion)

label_calendar = tk.Label(top_group, text=t('label_calendar'))
label_calendar.grid(row=0, column=0, sticky='e')
radio_solar = tk.Radiobutton(top_group, text=t('radio_solar'), variable=var, value='阳历', command=update_pillars_from_date)
radio_solar.grid(row=0, column=1, sticky='w')
radio_lunar = tk.Radiobutton(top_group, text=t('radio_lunar'), variable=var, value='农历', command=update_pillars_from_date)
radio_lunar.grid(row=0, column=2, sticky='w')
label_gender = tk.Label(top_group, text=t('label_gender'))
label_gender.grid(row=0, column=3, sticky='e', padx=(8, 0))
gender_var = tk.StringVar(value='男')
radio_male = tk.Radiobutton(top_group, text=t('radio_male'), variable=gender_var, value='男')
radio_male.grid(row=0, column=4, sticky='w')
radio_female = tk.Radiobutton(top_group, text=t('radio_female'), variable=gender_var, value='女')
radio_female.grid(row=0, column=5, sticky='w')

label_language = tk.Label(top_group, text=t('label_language'))
label_language.grid(row=0, column=6, sticky='e', padx=(8, 0))
language_choice_var = tk.StringVar(value='中国（大陆）')
combo_language = ttk.Combobox(
    top_group,
    textvariable=language_choice_var,
    values=list(COUNTRY_LANGUAGE_MAP.keys()),
    state='readonly',
    width=12,
)
combo_language.grid(row=0, column=7, sticky='w')
combo_language.bind('<<ComboboxSelected>>', on_language_select)

# 姓名（与 差异.docx image1 参考图一致；仅展示用，不影响排盘计算）
label_name = tk.Label(top_group, text='姓名')
label_name.grid(row=0, column=8, sticky='e', padx=(12, 0))
entry_name = tk.Entry(top_group, width=12)
entry_name.grid(row=0, column=9, sticky='w')
entry_name.insert(0, '')

month_method_var = tk.StringVar(value='定气法')

entry_year = tk.Entry(frame, width=6)
entry_year.grid(row=2, column=0)
label_year_unit = tk.Label(frame, text=ui_text('unit_year'))
label_year_unit.grid(row=2, column=1, sticky='w')
entry_month = tk.Entry(frame, width=3)
entry_month.grid(row=2, column=2)
label_month_unit = tk.Label(frame, text=ui_text('unit_month'))
label_month_unit.grid(row=2, column=3, sticky='w')
entry_day = tk.Entry(frame, width=3)
entry_day.grid(row=2, column=4)
label_day_unit = tk.Label(frame, text=ui_text('unit_day'))
label_day_unit.grid(row=2, column=5, sticky='w')
entry_hour = tk.Entry(frame, width=6)
entry_hour.grid(row=2, column=6)
label_hour_unit = tk.Label(frame, text=ui_text('unit_hour'))
label_hour_unit.grid(row=2, column=7, sticky='w')

summer_time_var = tk.BooleanVar(value=False)
summer_time_var.trace_add('write', update_true_solar_preview)
check_summer_time = tk.Checkbutton(
    frame,
    text=t('check_summer_time'),
    variable=summer_time_var,
)
check_summer_time.grid(row=3, column=8, columnspan=3, sticky='w', pady=(2, 0))
summer_time_hint_label = tk.Label(frame, text='', anchor='w', justify='left', fg='#8a4b08')
summer_time_hint_label.grid(row=3, column=11, columnspan=3, sticky='w', padx=(8, 0), pady=(2, 0))
# 真太阳时 / 地址经纬 实时预览（与 差异.docx image1 参考图一致：查询页即显示换算结果）
true_solar_preview_label = tk.Label(frame, text='', anchor='w', justify='left', fg='#2f5d2f')
true_solar_preview_label.grid(row=4, column=0, columnspan=14, sticky='we', padx=(6, 0), pady=(2, 0))

label_birthplace = tk.Label(frame, text=t('label_birthplace'))
label_birthplace.grid(row=2, column=8, sticky='e', padx=(6, 0))
entry_birthplace = tk.Entry(frame, width=14, state='readonly')
entry_birthplace.grid(row=2, column=9, sticky='w')
btn_pick_birthplace = tk.Button(frame, text=t('btn_pick_birthplace'), command=open_birthplace_selector)
btn_pick_birthplace.grid(row=2, column=10, sticky='w', padx=(4, 0))

entry_year.bind('<FocusOut>', lambda event: update_pillars_from_date())
entry_month.bind('<FocusOut>', lambda event: update_pillars_from_date())
entry_day.bind('<FocusOut>', lambda event: update_pillars_from_date())
entry_hour.bind('<FocusOut>', lambda event: update_pillars_from_date())
for _date_entry in (entry_year, entry_month, entry_day, entry_hour):
    _date_entry.bind('<FocusOut>', refresh_summer_time_suggestion, add='+')
refresh_summer_time_suggestion()

# 指定命宫 / 流年 / 平气·定气法：按《改写》参照图红框位置内联展示在主输入区；
# 四柱（自动填柱的可覆盖项）保留在可折叠“高级选项”内。
advanced_visible_var = tk.BooleanVar(value=False)
advanced_frame = tk.LabelFrame(frame, text='高级选项（四柱）')
advanced_frame.grid(row=7, column=0, columnspan=14, sticky='ew')
advanced_frame.grid_remove()

# 平气法 / 定气法：参照图位于顶部日期行最右侧（出生地选择按钮旁）
radio_pingqi = tk.Radiobutton(frame, text=t('radio_pingqi'), variable=month_method_var, value='平气法')
radio_pingqi.grid(row=2, column=11, sticky='w', padx=(6, 0))
radio_dingqi = tk.Radiobutton(frame, text=t('radio_dingqi'), variable=month_method_var, value='定气法')
radio_dingqi.grid(row=2, column=12, sticky='w')


def toggle_advanced_options():
    if advanced_visible_var.get():
        advanced_frame.grid()
    else:
        advanced_frame.grid_remove()


label_year_pillar = tk.Label(advanced_frame, text=ui_text('label_year_pillar'))
label_year_pillar.grid(row=0, column=0, sticky='e', padx=(6, 0), pady=4)
entry_year_pillar = PillarEntry(advanced_frame)
entry_year_pillar.grid(row=0, column=1)
label_month_pillar = tk.Label(advanced_frame, text=ui_text('label_month_pillar'))
label_month_pillar.grid(row=0, column=2, sticky='e', padx=(12, 0), pady=4)
entry_month_pillar = PillarEntry(advanced_frame)
entry_month_pillar.grid(row=0, column=3)
label_day_pillar = tk.Label(advanced_frame, text=ui_text('label_day_pillar'))
label_day_pillar.grid(row=0, column=4, sticky='e', padx=(12, 0), pady=4)
entry_day_pillar = DunPillarEntry(advanced_frame)
entry_day_pillar.grid(row=0, column=5)
label_hour_pillar = tk.Label(advanced_frame, text=ui_text('label_hour_pillar'))
label_hour_pillar.grid(row=0, column=6, sticky='e', padx=(12, 0), pady=4)
entry_hour_pillar = DunPillarEntry(advanced_frame)
entry_hour_pillar.grid(row=0, column=7)

for _pillar_entry in (entry_year_pillar, entry_month_pillar, entry_day_pillar, entry_hour_pillar):
    _inner = _pillar_entry.pillar if isinstance(_pillar_entry, DunPillarEntry) else _pillar_entry
    _inner.tg_entry.bind('<FocusOut>', lambda event: refresh_dun_display())
    _inner.dz_entry.bind('<FocusOut>', lambda event: refresh_dun_display())

# 指定命宫 / 流年年份：参照图位于四柱下行、按钮上行（红框位置），主输入区内联展示
label_specified_minggong = tk.Label(frame, text=ui_text('label_specified_minggong'))
label_specified_minggong.grid(row=5, column=0, sticky='e', padx=(6, 0), pady=4)
entry_specified_minggong = tk.Entry(frame, width=6)
entry_specified_minggong.grid(row=5, column=1)
label_flow_year = tk.Label(frame, text=ui_text('label_flow_year'))
label_flow_year.grid(row=5, column=2, sticky='e', padx=(12, 0), pady=4)
entry_flow_year = tk.Entry(frame, width=6)
entry_flow_year.grid(row=5, column=3)

btn_toggle_advanced = tk.Checkbutton(
    frame, text='高级选项', variable=advanced_visible_var, command=toggle_advanced_options
)
btn_toggle_advanced.grid(row=6, column=0, columnspan=14, sticky='w', pady=(6, 0))
# 与改写/差异文档一致：输入区只保留一个“排盘”按钮，点击后自动跳转到查询结果界面
# （基本命盘、普通排盘、禄命排盘 均在结果页签内展示）
btn_query = tk.Button(frame, text='开始排盘', command=start_chart_query)
btn_query.grid(row=8, column=0, columnspan=2, pady=10, sticky='w')

result_back_button = tk.Button(result_page, text='返回输入界面', command=show_input_page)
result_back_button.pack(anchor='w', padx=20, pady=(10, 0))
result_frame = tk.LabelFrame(result_page, text=ui_text('result_frame_title'))
result_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
result_notebook = ttk.Notebook(result_frame)
result_notebook.pack(fill='both', expand=True, padx=4, pady=4)

basic_result_frame = tk.Frame(result_notebook)
ordinary_result_frame = tk.Frame(result_notebook)
luming_result_frame = tk.Frame(result_notebook)
result_notebook.add(basic_result_frame, text='基本命盘')
result_notebook.add(ordinary_result_frame, text='普通排盘')
result_notebook.add(luming_result_frame, text='禄命排盘')
result_notebook.bind('<<NotebookTabChanged>>', on_result_tab_changed)

result_title_label = tk.Label(basic_result_frame, text=ui_text('result_display_area'), anchor='w')
result_title_label.pack(fill='x', padx=8, pady=(8, 0))
result_info_label = tk.Label(basic_result_frame, text='', anchor='w', justify='left')
result_info_label.pack(fill='x', padx=8, pady=(4, 8))

result_table_frame = tk.Frame(basic_result_frame)
result_table_frame.pack(fill='both', expand=True, padx=8, pady=4)
columns = [ui_text('table_item')] + ui_month_headers()
result_table = ttk.Treeview(result_table_frame, columns=columns, show='headings')
for i, col in enumerate(columns):
    result_table.heading(col, text=col)
    width = 110 if i == 0 else 80
    result_table.column(col, width=width, anchor='center')
result_table.pack(side='left', fill='both', expand=True)

scrollbar_v = tk.Scrollbar(result_table_frame, orient='vertical', command=result_table.yview)
scrollbar_v.pack(side='right', fill='y')
result_table.config(yscrollcommand=scrollbar_v.set)
scrollbar_h = tk.Scrollbar(result_table_frame, orient='horizontal', command=result_table.xview)
scrollbar_h.pack(fill='x')
result_table.config(xscrollcommand=scrollbar_h.set)

result_ordinary_title_label = tk.Label(ordinary_result_frame, text='普通排盘', anchor='w')
result_ordinary_title_label.pack(fill='x', padx=8, pady=(8, 0))
result_ordinary_info_label = tk.Label(ordinary_result_frame, text='', anchor='w', justify='left')
result_ordinary_info_label.pack(fill='x', padx=8, pady=(4, 8))
# 横向流月条（置于下方网格之下）：默认显示“当下时间年份”的流月，选中流年格时即时切换
ordinary_flow_month_frame, ordinary_flow_month_update, ordinary_flow_month_cells = create_flow_month_strip(ordinary_result_frame)
# 大运密集网格（参照图格式）：顶行大运链 + 每步大运一行（块头 + 10 个流年格）
ordinary_grid_holder = tk.Frame(ordinary_result_frame)


def ordinary_on_year_select(year, block_row):
    ordinary_flow_month_update.set_step(format_dayun_step_text(block_row))
    ordinary_flow_month_update(year)


ordinary_flow_grid = DayunFlowGrid(ordinary_grid_holder, on_year_select=ordinary_on_year_select)
ordinary_flow_grid.pack(fill='both', expand=True)
ordinary_grid_holder.pack(fill='both', expand=True, padx=8, pady=4)
ordinary_flow_month_frame.pack(fill='x', padx=8, pady=(4, 8))

luming_options = tk.Frame(luming_result_frame)
luming_options.pack(anchor='nw', padx=12, pady=(6, 6))
tk.Label(luming_options, text='排盘基准：').grid(row=0, column=0, sticky='w', pady=2)
luming_base_var = tk.StringVar(value='日柱排盘')
for column, label in enumerate(('年柱排盘', '月柱排盘', '日柱排盘', '时柱排盘'), start=1):
    tk.Radiobutton(luming_options, text=label, variable=luming_base_var, value=label).grid(
        row=0, column=column, sticky='w', padx=4
    )
tk.Label(luming_options, text='指定太极点：').grid(row=1, column=0, sticky='w', pady=2)
luming_taiji_var = tk.StringVar(value='癸')
ttk.Combobox(
    luming_options, textvariable=luming_taiji_var,
    values=('甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'),
    state='readonly', width=5,
).grid(row=1, column=1, sticky='w')
tk.Label(luming_options, text='大运取柱：').grid(row=2, column=0, sticky='w', pady=2)
luming_dayun_var = tk.StringVar(value='月柱排大运')
for column, label in enumerate(('年柱排大运', '月柱排大运', '日柱排大运', '时柱排大运'), start=1):
    tk.Radiobutton(luming_options, text=label, variable=luming_dayun_var, value=label).grid(
        row=2, column=column, sticky='w', padx=4
    )
tk.Label(luming_options, text='大运方向：').grid(row=3, column=0, sticky='w', pady=2)
luming_direction_var = tk.StringVar(value='大运顺排')
tk.Radiobutton(luming_options, text='大运顺排', variable=luming_direction_var, value='大运顺排').grid(row=3, column=1, sticky='w')
tk.Radiobutton(luming_options, text='大运逆排', variable=luming_direction_var, value='大运逆排').grid(row=3, column=2, sticky='w')
tk.Button(luming_options, text='按所选条件排盘', command=query_luming).grid(
    row=4, column=0, columnspan=3, sticky='w', pady=(4, 0)
)
luming_result_info_label = tk.Label(luming_result_frame, text='', anchor='w', justify='left')
luming_result_info_label.pack(fill='x', padx=12, pady=(0, 8))
# 横向流月条（置于下方网格之下）：默认显示“当下时间年份”的流月，选中流年格时即时切换
luming_flow_month_frame, luming_flow_month_update, luming_flow_month_cells = create_flow_month_strip(luming_result_frame)
# 大运密集网格（参照图格式）：顶行大运链 + 每步大运一行（块头 + 10 个流年格）
luming_grid_holder = tk.Frame(luming_result_frame)


def luming_on_year_select(year, block_row):
    luming_flow_month_update.set_step(format_dayun_step_text(block_row))
    luming_flow_month_update(year)


luming_flow_grid = DayunFlowGrid(luming_grid_holder, on_year_select=luming_on_year_select)
luming_flow_grid.pack(fill='both', expand=True)
luming_grid_holder.pack(fill='both', expand=True, padx=12, pady=(0, 4))
luming_flow_month_frame.pack(fill='x', padx=12, pady=(4, 8))

if __name__ == '__main__':
    root.mainloop()
