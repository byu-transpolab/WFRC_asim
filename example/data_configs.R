library(sf)
library(tidyverse)
library(data.table)
as_persons <- read_csv("data/synthetic_persons.csv")
as_persons$perid <- 1:nrow(as_persons)
as_persons <- as_persons %>% 
  setnames("AGEP", "age") %>% 
  setnames("SEX", "sex")
write_csv(as_persons, "data/synthetic_persons2.csv")
