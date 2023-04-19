import pandas as pd

# Load the CSV file into a pandas DataFrame
csv_file_path = 'data/LLCP2021.csv'
df = pd.read_csv(csv_file_path)
# print(df)
brfss_df_selected = df[['_MICHD', '_RFHYPE6', 'TOLDHI3', '_CHOLCH3', '_BMI5', 'SMOKE100', 'CVDSTRK3', 'PREDIAB1', '_TOTINDA', '_FRTLT1A', '_VEGLT1A', '_RFDRHV7', 'MEDCOST1', 'GENHLTH', 'MENTHLTH', 'PHYSHLTH', 'DIFFWALK', 'SEXVAR', '_AGEG5YR', 'EDUCA', 'INCOME3','_HCVU652','ASTHMA3','CHCSCNCR','_IMPRACE','CHCKDNY2','_RFBMI5']]

#Drop Missing Values - knocks 100,000 rows out right away
brfss_df_selected = brfss_df_selected.dropna()

# _MICHD
#Change 2 to 0 because this means did not have MI(myocardial infarction) or CHD (coronary heart disease)
brfss_df_selected['_MICHD'] = brfss_df_selected['_MICHD'].replace({2: 0})
brfss_df_selected._MICHD.unique()

#1 _RFHYPE6
#Change 1 to 0 so it represetnts No high blood pressure and 2 to 1 so it represents high blood pressure
brfss_df_selected['_RFHYPE6'] = brfss_df_selected['_RFHYPE6'].replace({1:0, 2:1})
brfss_df_selected = brfss_df_selected[brfss_df_selected._RFHYPE6 != 9]
brfss_df_selected._RFHYPE6.unique()

#2 TOLDHI3
# Change 2 to 0 because it is No
# Remove all 7 (dont knows)
# Remove all 9 (refused)
brfss_df_selected['TOLDHI3'] = brfss_df_selected['TOLDHI3'].replace({2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.TOLDHI3 != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.TOLDHI3 != 9]
brfss_df_selected.TOLDHI3.unique()

#3 _CHOLCH3
# Change 3 to 0 and 2 to 0 for Not checked cholesterol in past 5 years
# Remove 9
brfss_df_selected['_CHOLCH3'] = brfss_df_selected['_CHOLCH3'].replace({3:0,2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected._CHOLCH3 != 9]
brfss_df_selected._CHOLCH3.unique()

#4 _BMI5 (no changes, just note that these are BMI * 100. So for example a BMI of 4018 is really 40.18)
brfss_df_selected['_BMI5'] = brfss_df_selected['_BMI5'].div(100).round(0)
brfss_df_selected._BMI5.unique()

#5 SMOKE100
# Change 2 to 0 because it is No
# Remove all 7 (dont knows)
# Remove all 9 (refused)
brfss_df_selected['SMOKE100'] = brfss_df_selected['SMOKE100'].replace({2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.SMOKE100 != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.SMOKE100 != 9]
brfss_df_selected.SMOKE100.unique()

#6 CVDSTRK3
# Change 2 to 0 because it is No
# Remove all 7 (dont knows)
# Remove all 9 (refused)
brfss_df_selected['CVDSTRK3'] = brfss_df_selected['CVDSTRK3'].replace({2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.CVDSTRK3 != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.CVDSTRK3 != 9]
brfss_df_selected.CVDSTRK3.unique()

#7 PREDIAB1 -Diabetes
# going to make this ordinal. 0 is for no diabetes or only during pregnancy, 1 is for pre-diabetes or borderline diabetes, 2 is for yes diabetes
# Remove all 7 (dont knows)
# Remove all 9 (refused)
brfss_df_selected['PREDIAB1'] = brfss_df_selected['PREDIAB1'].replace({2:0, 3:0, 1:2, 4:1})
brfss_df_selected = brfss_df_selected[brfss_df_selected.PREDIAB1 != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.PREDIAB1 != 9]
brfss_df_selected.PREDIAB1.unique()

#8 _TOTINDA
# 1 for physical activity
# change 2 to 0 for no physical activity
# Remove all 9 (don't know/refused)
brfss_df_selected['_TOTINDA'] = brfss_df_selected['_TOTINDA'].replace({2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected._TOTINDA != 9]
brfss_df_selected._TOTINDA.unique()

#9 _FRTLT1A
# Change 2 to 0. this means no fruit consumed per day. 1 will mean consumed 1 or more pieces of fruit per day 
# remove all dont knows and missing 9
brfss_df_selected['_FRTLT1A'] = brfss_df_selected['_FRTLT1A'].replace({2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected._FRTLT1A != 9]
brfss_df_selected._FRTLT1A.unique()

#10 _VEGLT1A
# Change 2 to 0. this means no vegetables consumed per day. 1 will mean consumed 1 or more pieces of vegetable per day 
# remove all dont knows and missing 9
brfss_df_selected['_VEGLT1A'] = brfss_df_selected['_VEGLT1A'].replace({2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected._VEGLT1A != 9]
brfss_df_selected._VEGLT1A.unique()

#11 _RFDRHV7
# Change 1 to 0 (1 was no for heavy drinking). change all 2 to 1 (2 was yes for heavy drinking)
# remove all dont knows and missing 9
brfss_df_selected['_RFDRHV7'] = brfss_df_selected['_RFDRHV7'].replace({1:0, 2:1})
brfss_df_selected = brfss_df_selected[brfss_df_selected._RFDRHV7 != 9]
brfss_df_selected._RFDRHV7.unique()

#12  _HCVU652
# 1 is yes, change 2 to 0 because it is No health care access
# remove 7 and 9 for don't know or refused
brfss_df_selected['_HCVU652'] = brfss_df_selected['_HCVU652'].replace({2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected._HCVU652 != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected._HCVU652 != 9]
brfss_df_selected._HCVU652.unique()

#13 MEDCOST1
# Change 2 to 0 for no, 1 is already yes
# remove 7 for don/t know and 9 for refused
brfss_df_selected['MEDCOST1'] = brfss_df_selected['MEDCOST1'].replace({2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.MEDCOST1 != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.MEDCOST1 != 9]
brfss_df_selected.MEDCOST1.unique()

#14 GENHLTH
# This is an ordinal variable that I want to keep (1 is Excellent -> 5 is Poor)
# Remove 7 and 9 for don't know and refused
brfss_df_selected = brfss_df_selected[brfss_df_selected.GENHLTH != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.GENHLTH != 9]
brfss_df_selected.GENHLTH.unique()

#15 MENTHLTH
# already in days so keep that, scale will be 0-30
# change 88 to 0 because it means none (no bad mental health days)
# remove 77 and 99 for don't know not sure and refused
brfss_df_selected['MENTHLTH'] = brfss_df_selected['MENTHLTH'].replace({88:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.MENTHLTH != 77]
brfss_df_selected = brfss_df_selected[brfss_df_selected.MENTHLTH != 99]
brfss_df_selected.MENTHLTH.unique()

#16 PHYSHLTH
# already in days so keep that, scale will be 0-30
# change 88 to 0 because it means none (no bad mental health days)
# remove 77 and 99 for don't know not sure and refused
brfss_df_selected['PHYSHLTH'] = brfss_df_selected['PHYSHLTH'].replace({88:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.PHYSHLTH != 77]
brfss_df_selected = brfss_df_selected[brfss_df_selected.PHYSHLTH != 99]
brfss_df_selected.PHYSHLTH.unique()

#17 DIFFWALK
# change 2 to 0 for no. 1 is already yes
# remove 7 and 9 for don't know not sure and refused
brfss_df_selected['DIFFWALK'] = brfss_df_selected['DIFFWALK'].replace({2:0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.DIFFWALK != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.DIFFWALK != 9]
brfss_df_selected.DIFFWALK.unique()

#18 SEXVAR
# in other words - is respondent male (somewhat arbitrarily chose this change because men are at higher risk for heart disease)
# change 2 to 0 (female as 0). Male is 1
brfss_df_selected['SEXVAR'] = brfss_df_selected['SEXVAR'].replace({2:0})
brfss_df_selected.SEXVAR.unique()

#19 _AGEG5YR
# already ordinal. 1 is 18-24 all the way up to 13 wis 80 and older. 5 year increments.
# remove 14 because it is don't know or missing
brfss_df_selected = brfss_df_selected[brfss_df_selected._AGEG5YR != 14]
brfss_df_selected._AGEG5YR.unique()

#20 EDUCA
# This is already an ordinal variable with 1 being never attended school or kindergarten only up to 6 being college 4 years or more
# Scale here is 1-6
# Remove 9 for refused:
brfss_df_selected = brfss_df_selected[brfss_df_selected.EDUCA != 9]
brfss_df_selected.EDUCA.unique()

#21 INCOME3
# Variable is already ordinal with 1 being less than $10,000 all the way up to 8 being $75,000 or more
# Remove 77 and 99 for don't know and refused
brfss_df_selected = brfss_df_selected[brfss_df_selected.INCOME3 != 77]
brfss_df_selected = brfss_df_selected[brfss_df_selected.INCOME3 != 99]
brfss_df_selected.INCOME3.unique()

#22 CHCSCNCR- cancer
brfss_df_selected['CHCSCNCR'] = brfss_df_selected['CHCSCNCR'].replace({2: 0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.CHCSCNCR != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.CHCSCNCR != 9]
brfss_df_selected.CHCSCNCR.unique()

#23 ASTHMA3- Asthama

brfss_df_selected['ASTHMA3'] = brfss_df_selected['ASTHMA3'].replace({2: 0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.ASTHMA3 != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.ASTHMA3 != 9]
brfss_df_selected.ASTHMA3.unique()

#24 _RFBMI5- Obese

brfss_df_selected['_RFBMI5'] = brfss_df_selected['_RFBMI5'].replace({1:0, 2:1})
brfss_df_selected = brfss_df_selected[brfss_df_selected._RFBMI5 != 9]
brfss_df_selected._RFBMI5.unique()

#25 CHCKDNY2 - Kidney Disorder

brfss_df_selected['CHCKDNY2'] = brfss_df_selected['CHCKDNY2'].replace({2: 0})
brfss_df_selected = brfss_df_selected[brfss_df_selected.CHCKDNY2 != 7]
brfss_df_selected = brfss_df_selected[brfss_df_selected.CHCKDNY2 != 9]
brfss_df_selected.CHCKDNY2.unique()

##### Make Feature Names More Readable
brfss_cleaned = brfss_df_selected.rename(columns = {'_MICHD':'HeartDiseaseorAttack', 
                                         '_RFHYPE6':'High BP',  
                                         'TOLDHI3':'High Cholesterol', '_CHOLCH3':'Cholesterol Check', 
                                         '_BMI5':'BMI', 
                                         'SMOKE100':'Smoker', 
                                         'CVDSTRK3':'Stroke', 'PREDIAB1':'Diabetes', 
                                         'CHCKDNY2':'Kidney Disease', '_IMPRACE':'Race', 
                                         'ASTHMA3':'Asthama', 'CHCSCNCR':'Skin Cancer',
                                         '_TOTINDA':'Physical Activity', 
                                         '_FRTLT1A':'Fruits', '_VEGLT1A':"Veggies", 
                                         '_RFDRHV7':'HeavyAlcoholConsump','_RFBMI5':'Obese', 
                                         '_HCVU652':'AnyHealthcare', 'MEDCOST1':'NoDocbcozCost', 
                                         'GENHLTH':'General Health', 'MENTHLTH':'Mental Health', 'PHYSHLTH':'PhysicalHlth', 'DIFFWALK':'DifficultyWalk', 
                                         'SEXVAR':'Sex', '_AGEG5YR':'Age', 'EDUCA':'Education', 'INCOME3':'Income' })

brfss_cleaned.to_csv('brfssCleaned.csv', index=False)

