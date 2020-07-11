library(sf)
library(tidyverse)
library(data.table)
library(omxr)

##Add necessary columns to persons for ActivtySim, update TAZ numbers
as_persons <- read_csv("data/synthetic_persons.csv")
as_persons$perid <- 1:nrow(as_persons)
as_persons <- as_persons %>% 
  setnames("AGEP", "age") %>% 
  setnames("SEX", "sex") %>% 
  mutate(
    ptype = case_when(
      age >= 18 & SCH == 1 & WKHP >= 30 ~ 1,
      age >= 18 & SCH == 1 & WKHP > 0 & WKHP < 30 ~ 2,
      age >= 18 & age < 65 & SCH == 1 & ESR == 3 | age >= 18 & age < 65 & SCH == 1 & ESR == 6 ~ 4,
      age >= 65 & SCH == 1 & ESR == 3 | age >= 65 & SCH == 1 & ESR == 6 ~ 5,
      age >= 18 & SCH == 2 | age >= 18 & SCH == 3 ~ 3,
      age > 15 & age < 18 ~ 6,
      age > 5 & age < 16 ~ 7,
      age >= 0 & age < 6 ~ 8
    ),
    pstudent = case_when(
      SCHG >= 2 & SCHG <= 14 ~ 1,
      SCHG > 14 & SCHG <= 16 ~ 2,
      T ~ 3
    ),
    pemploy = case_when(
      WKHP >= 30 ~ 1,
      WKHP > 0 & WKHP < 30 ~ 2,
      age >= 16 & ESR == 3 | age >= 16 & ESR == 6 ~ 3,
      T ~ 4
    ),
    TAZ2 = case_when(
      TAZ < 136 ~ TAZ,
      TAZ > 140 & TAZ < 421 ~ (TAZ - 5),
      TAZ > 422 & TAZ < 1782 ~ (TAZ -7),
      T ~ (TAZ - 14)
    )
  ) %>% 
  subset(select = -c(TAZ)) %>% 
  rename(TAZ = TAZ2)

write_csv(as_persons, "data/synthetic_persons2.csv")

##Rename household columns and update TAZ numbering
as_hh <- read_csv("data/synthetic_households.csv") %>% 
  mutate(income = round(HHINCADJ * (10^(-6))), digits = 0) %>% 
  setnames("NP", "hhsize") %>% 
  setnames("WIF", "num_workers") %>% 
  setnames("VEH", "VEHICL") %>% 
  mutate(
    TAZ2 = case_when(
      TAZ < 136 ~ TAZ,
      TAZ > 140 & TAZ < 421 ~ (TAZ - 5),
      TAZ > 422 & TAZ < 1782 ~ (TAZ -7),
      T ~ (TAZ - 14)
    )
  ) %>% 
  subset(select = -c(TAZ)) %>% 
  rename(TAZ = TAZ2)

write_csv(as_hh, "data/synthetic_households2.csv")

##Update ZONE numbers for SE data
SE <- read_csv("data/SE_Data.csv") %>% 
  mutate(
    ZONE2 = case_when(
      ZONE < 136 ~ ZONE,
      ZONE > 140 & ZONE < 421 ~ (ZONE - 5),
      ZONE > 422 & ZONE < 1782 ~ (ZONE -7),
      T ~ (ZONE - 14)
    )
  ) %>% 
  subset(select = -c(ZONE)) %>% 
  rename(ZONE = ZONE2)

write_csv(SE, "data/land_use_taz.csv")