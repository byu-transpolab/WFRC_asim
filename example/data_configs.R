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
    )
  )
write_csv(as_persons, "data/synthetic_persons2.csv")

as_hh <- read_csv("data/synthetic_households.csv") %>% 
  mutate(income = round(HHINCADJ * (10^(-6))), digits = 0)
write_csv(as_hh, "data/synthetic_households2.csv")