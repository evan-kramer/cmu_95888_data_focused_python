# Assignment 5
# Evan Kramer

library(tidyverse); library(lubridate)
setwd("C:/Users/evan.kramer/Documents/CMU/Courses/2020-03/95888 - Data Focused Python/Assignments/Assignment 5")
file = read_lines('expenses.txt')
pat = "[A-Z]"

# Loop
for(line in 1:length(file)) {
  if(str_count(file[line], pat) == 0) {
    print(file[line])
  } 
}

tibble(file) %>% 
  separate(file, into = str_c('v', 1:4), sep = ':') %>% 
  # filter(str_detect(v4, "a") & str_detect(v4, as.character(0:9)))
  filter(str_detect(v4, as.character(0:9)))

