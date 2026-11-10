"""Cited published Yemen indicators for the portfolio dashboards.
Not a live feed: explicitly label dates, geography, projections and sample coverage.
"""
SOURCES = {
  "OCHA_2026": {
    "title": "OCHA Yemen Humanitarian Needs and Response Plan 2026",
    "url": "https://yemen.un.org/ar/node/312711",
    "period": "2026-03",
    "scope": "Yemen national planning figures"
  },
  "WHO_2026": {
    "title": "WHO - Yemen health service functionality, October 2026",
    "url": "https://yemen.un.org/en/323279-who-scales-health-response-escalating-conflict-deepens-health-needs-yemen",
    "period": "2026-10",
    "scope": "5,415 assessed service units nationally; percentages rounded"
  },
  "UNFPA_2026": {
    "title": "UNFPA Yemen humanitarian situation January-March 2026",
    "url": "https://www.unfpa.org/resources/situation-report-crisis-yemen-%E2%80%93-january-march-2026",
    "period": "2026-03",
    "scope": "UNFPA-specific appeal, not total Yemen health funding"
  },
  "UNICEF_2026": {
    "title": "UNICEF Humanitarian Action for Children Yemen 2026",
    "url": "https://www.unicef.org/media/179566/file/2026-HAC-Yemen.pdf",
    "period": "2026",
    "scope": "National humanitarian planning estimate"
  },
  "STC_2026": {
    "title": "Save the Children - Barriers to Education (Aden, Lahj, Taiz)",
    "url": "https://resourcecentre.savethechildren.net/document/vulnerabilities-assessment-barriers-to-education-in-conflict-affected-communities-yemen-2026",
    "period": "2026",
    "scope": "Sample of 4,933 school-age children in three governorates; NOT national"
  },
  "FAO_2026": {
    "title": "FAO GIEWS Yemen Country Brief (13 October 2026)",
    "url": "https://www.fao.org/giews/countrybrief/country.jsp?code=YE",
    "period": "2026-10-13",
    "scope": "2026 food security forecast for GoY areas; August 2026 market quotes"
  },
  "IMF_2026": {
    "title": "IMF October 2026 World Economic Outlook - Yemen",
    "url": "https://www.imf.org/external/datamapper/profile/YEM",
    "period": "2026-10",
    "scope": "Forecast values; WEO figures may vary by coverage from World Bank/UN series"
  },
  "IMF_SMP_2026": {
    "title": "IMF October 7 2026 statement on Yemen",
    "url": "https://www.imf.org/en/news/articles/2026/10/07/pr26324-imf-management-approves-a-staff-monitored-program-with-yemen",
    "period": "2026-10-07",
    "scope": "2026 real GDP projection"
  },
  "WORLD_BANK_2026": {
    "title": "World Bank - Yemen Economic Monitor Spring 2026",
    "url": "https://www.worldbank.org/en/news/press-release/2026/05/21/economic-strain-deepens-in-yemen-as-regional-risks-intensify",
    "period": "2026-05-21",
    "scope": "2025 real GDP growth estimate, not 2026 projection"
  },
  "WORLD_BANK_POP": {
    "title": "World Bank - Population of Yemen, 2025",
    "url": "https://data.worldbank.org/indicator/SP.POP.TOTL?locations=YE",
    "period": "2025",
    "scope": "Population annual series, latest 2025"
  },
  "OCHA_EDUCATION": {
    "title": "OCHA Yemen HNRP 2026 - education needs and targeting",
    "url": "https://yemen.un.org/sites/default/files/2026-03/Yemen_2026_HNRP_EN_final.pdf",
    "period": "2026",
    "scope": "Education sector planning targets (not actual attendance)"
  }
}
HEALTH = {
 "population": 41773878,
 "measles_suspected_2026_min": 18000,
 "acute_malnutrition_under5": 2200000,
 "unfpa_funding_gap_usd": 62900000,
 "health_units_assessed": 5415,
 "facility_functionality_pct": {"full":60, "partial":35, "nonfunctional":4},
 "people_in_need_2026":22300000,
 "people_targeted_2026":12000000,
 "severe_acute_malnutrition":516157
}
EDUCATION = {
 "national_education_needs":6600000,
 "national_out_of_school":4500000,
 "education_target_children":1300000,
 "education_target_teachers":14500,
 "survey_children":4933,
 "survey_households":2225,
 "survey_out_of_school_pct":63,
 "survey_never_enrolled":1583,
 "survey_dropped_out":1287
}
ECONOMY = {
 "imf_nominal_gdp_2026_bn":10.98,
 "imf_inflation_2026_pct":5.0,
 "gdp_growth_2025_wb_pct":-1.5,
 "gdp_growth_2026_imf_pct":-1.5,
 "current_account_pct_gdp_2026":-3.3,
 "fiscal_balance_pct_gdp_2026":-0.4,
 "aden_fx_2026_aug_yer_per_usd":1555,
 "food_yoy_aug_2026_pct":{"imported_wheat_flour":-1,"basmati_rice":-5,"min_food_basket":-2},
 "fao_goy_ipc3plus_oct_dec_2026_m":5.4,
 "fao_goy_ipc4_oct_dec_2026_m":1.8,
 "ocha_plan_2026_usd_bn":2.16,
 "ocha_prioritized_usd_bn":1.6
}
