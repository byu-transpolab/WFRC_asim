library(sf)
library(tidyverse)
library(data.table)
as_persons <- read_csv("data/synthetic_persons.csv")
as_persons$perid <- 1:nrow(as_persons)
as_persons <- as_persons %>% 
  setnames("AGEP", "age") %>% 
  setnames("SEX", "sex") %>% 
  mutate(
    ptype = case_when(
      age >= 18 & SCH == 1 & WKHP >= 30 ~ 1,
      age >= 18 & SCH == 1 & WKHP > 0 & WKHP < 30 ~ 2,
      age >= 18 & age < 65 & SCH == 1 & ESR == 3 | age >= 18 & age < 65 & SCH == 1 & ESR == 6 ~ 3,
      age >= 65 & SCH == 1 & ESR == 3 | age >= 65 & SCH == 1 & ESR == 6 ~ 4,
      age >= 18 & SCH == 2 | age >= 18 & SCH == 3 ~ 5,
      age > 15 & age < 18 ~ 6,
      age > 5 & age < 16 ~ 7,
      age >= 0 & age < 6 ~ 8
    )
  )
#write_csv(as_persons, "data/synthetic_persons2.csv")





people <- read_csv("output/synthetic_persons.csv")

people <- people %>% 
  mutate_at(.vars = vars(COW, WKHP, DDRS, DIS), replace_na) %>% 
  mutate(
    DIS_status = case_when(
      DDRS == "1" ~ T,
      TRUE ~ F
    ),
    PT_hours = case_when(
      WKHP > 0 & WKHP < 30 ~ T,
      TRUE ~ F
    ),
    FT_hours = case_when(
      between(WKHP, 30, 99) ~ T,
      TRUE ~ F
    ), 
    worker = case_when(
      PT_hours == TRUE ~ T,
      FT_hours == T ~ T,
      T ~ F
    ),
    
    person_type = case_when(
      DIS_status == T & worker == T ~ "WW",
      DIS_status == T & worker == F ~ "WN",
      FT_hours == T ~ "FW",
      PT_hours == T ~ "PW",
      COW == "9" & AGEP >= 50 ~ "RT", 
      worker == F & AGEP >= 18 ~ "NW",
      AGEP < 18 & AGEP >= 16 ~ "SD",
      AGEP < 16 & AGEP >= 5  ~ "SP",
      AGEP >= 0 & AGEP < 5 ~ "PS",
      T ~ "NONE"
    ),
    person_type = fct_relevel(person_type, 
                              "FW", "PW", "NW", "RT", 
                              "SD", "SP", "PS", "WW", "WN", "NONE")
  )
