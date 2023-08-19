import pandas as pd
from bs4 import BeautifulSoup
import json

def des_parse_html(des_html_content):
  soup = BeautifulSoup(des_html_content, 'html.parser')
  # Extract relevant information
  data = {}

  # Extract Description
  description = soup.find('label', text='Description')
  if description:
      description_content = description.find_next('div', class_='text-left float-label-left').text.strip()
      data['Description'] = description_content

  # Extract Designer/Maker
  designer_maker = soup.find('label', text='Designer/Maker')
  if designer_maker:
      designer_maker_content = designer_maker.find_next('div', class_='text-left float-label-left').text.strip()
      data['designer'] = designer_maker_content

  # Extract Builder/Maker
  builder_maker = soup.find('label', text='Builder/Maker')
  if builder_maker:
      builder_maker_content = builder_maker.find_next('div', class_='text-left float-label-left').text.strip()
      data['builder'] = builder_maker_content

  # Extract Construction Year Start & End
  construction_year = soup.find('label', text='Construction Year Start & End')
  if construction_year:
      construction_year_content = construction_year.find_next('div', class_='text-left float-label-left').text.strip()
      data['constructionYear'] = construction_year_content

  # Extract Physical Description
  physical_description = soup.find('label', text='Physical Description')
  if physical_description:
      physical_description_content = physical_description.find_next('textarea').text.strip()
      data['physicalDescription'] = physical_description_content

  # Extract Physical Condition and/or Archaeological Potential
  condition_potential = soup.find('label', text='Physical Condition and/or Archaeological Potential')
  if condition_potential:
      condition_potential_content = condition_potential.find_next('textarea').text.strip()
      data['physicalCondition'] = condition_potential_content

  # Extract Modifications & Dates
  modifications_dates = soup.find('label', text='Modifications & Dates')
  if modifications_dates:
      modifications_dates_content = modifications_dates.find_next('textarea').text.strip()
      data['modifyDates'] = modifications_dates_content

# Extract further comments
  further_comments=soup.find('label', _for='Further_Comments')
  if further_comments:
    further_comments_content = further_comments.find_next('label').text.strip()
    data['furtherComments'] = further_comments_content

  # Extract Current Use
  current_use = soup.find('label', text='Current Use')
  if current_use:
      current_use_content = current_use.find_next('label').text.strip()
      data['currentUse'] = current_use_content

  # Extract Former Use
  former_use = soup.find('label', text='Former Use')
  if former_use:
      former_use_content = former_use.find_next('label').text.strip()
      data['formerUse'] = former_use_content

  # Print or save the extracted data as JSON
  des_json_data = json.dumps(data, indent=4, ensure_ascii=False)

  return des_json_data

def sig_parse_html(sig_html_content):
  # Parse the HTML using BeautifulSoup
  soup = BeautifulSoup(sig_html_content, 'html.parser')

  # Initialize a dictionary to store the extracted data
  data = {}

  #Statement of Significance
  statement_of_significance = soup.find('label', text='Statement of Significance')
  if statement_of_significance:
      statement_content = statement_of_significance.find_next('textarea', id='Entity_StatementOfSignificance').text.strip()
      data['statementSignificance'] = statement_content

  #DateSignificanceUpdated
  date_significance_updated = soup.find('label', text='Date Significance Updated :')
  if date_significance_updated:
      date_updated = date_significance_updated.find_next('label', style='font-weight: normal;').text.strip()
      data['updateDate']= date_updated

  #AestheticSignificance
  aesthetic_significance = soup.find('label', text='SHR Criteria c)')
  if aesthetic_significance:
      aesthetic_content = aesthetic_significance.find_next('textarea', id='ItemAssessmentViewModel_Entity_AestheticSignificance').text.strip()
      data['aestheticSignificance'] = aesthetic_content

  #Social Significance
  social_sig=soup.find('textarea', id='ItemAssessmentViewModel_Entity_CulturalSignificance')
  if social_sig:
      social_sig_content=soup.find('textarea', id='ItemAssessmentViewModel_Entity_CulturalSignificance').text.strip()
      data['aestheticSignificance'] = social_sig_content

#Rare Assessment
  rare_ass=soup.find('textarea', id='ItemAssessmentViewModel_Entity_Rarity')
  if rare_ass:
      rare_ass_content=soup.find('textarea', id='ItemAssessmentViewModel_Entity_Rarity').text.strip()
      data['rareAssessment'] = rare_ass_content

  # Extract Research Significance
  research_significance = soup.find('label', text='SHR Criteria e)')
  if research_significance:
      research_content = research_significance.find_next('textarea', id='ItemAssessmentViewModel_Entity_ResearchPotential').text.strip()
      data['researchSignificance'] = research_content

  # Extract Integrity/Intactness
  integrity_intactness = soup.find('label', text='Integrity/Intactness')
  if integrity_intactness:
      integrity_content = integrity_intactness.find_next('textarea', id='ItemAssessmentViewModel_Entity_Intactness').text.strip()
      data['integrity'] = integrity_content

  # Extract Historical Significance
  historical_significance = soup.find('label', text='SHR Criteria a)')
  if historical_significance:
      historical_content = historical_significance.find_next('textarea', id='ItemAssessmentViewModel_Entity_HistoricalSignificance').text.strip()
      data['historicalSignificance'] = historical_content

  sig_json_data = json.dumps(data, indent=4)

  return sig_json_data