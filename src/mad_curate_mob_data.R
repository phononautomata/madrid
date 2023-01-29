# This script collects the mobility data of the so-called 'reference period'
# as referred to by the Ministry of Transport. This reference period is involves
# a few days of mobility data before the activation of the generalized lockdowns
# across Spain.

# In order for the script to work properly, the raw data from the
# Ministry of Transport has to be stored where the lower_path says.

# The output of this script is a single csv file. The csv file is a 
# 21 x 21 table, where every element  (ij) represents the mean total number of 
# travels that took place between districts i and j according to the raw data
# averaged over the reference period. The mobility matrix of the model for 
# Madrid's perimeter lockdowns is informed using this data.

library("dplyr")

path <- setwd("~/madrid")
lower_path <- 'madrid/data/0000_referencia_maestra1_mitma_distrito/'
full_path <- file.path(path, lower_path)

#low_path = '/citymob/data/0000_referencia_maestra1_mitma_distrito/' # TO BE GENERALIZED
#folder_path = paste(new_wd,low_path,sep="")

day_list = c(14, 15, 16, 17, 18, 19, 20) # Days of the reference period
L = length(day_list) 

ref_week_travel_matrix<-matrix(0, nrow=21, ncol=21)

for (day in day_list) {
  
  # Paste full date string
  yearmonth = 202002 # TO BE GENERALIZED
  full_date = paste(yearmonth,day,sep="")
  
  # Prepare full file name, read txt file and replace symbols
  file_name_ending = '_maestra_1_mitma_distrito.txt'
  file_name = paste(full_date, file_name_ending,sep="")
  full_name = paste(full_path,file_name,sep="")
  
  tx <- readLines(full_name)
  tx2 <- gsub(pattern ="|", replace = ",", x = tx, fixed = TRUE)
  
  # Create new changed file and save as csv
  file_name_ending2 = '_maestra_1_mitma_distrito.csv'
  file_name2 = paste(full_date, file_name_ending2,sep="")
  full_name2 = paste(full_path,file_name2,sep="")
  
  writeLines(tx2, con=full_name2)
  
  # Read csv as dataframe, check variable type
  
  mob_data <- read.csv(full_name2, header = TRUE, sep = ",")
  
  sapply(mob_data, class)
  
  # Change 'origen' & 'destino' columns from character to numeric
  i <- c(2, 3)
  mob_data[ , i] <- apply(mob_data[ , i], 2, 
                          function(x) as.numeric(as.character(x)))
  
  sapply(mob_data, class)
  
  # Filter travels within city districts 
  # MAD: CPRO=28, CMUN=079, CSEC=01 to 21
  CPRO = 28
  CMUN = 079
  
  mad_mob_data <- filter(mob_data, 2807900 < mob_data$origen)
  mad_mob_data <- filter(mad_mob_data, mad_mob_data$origen < 2807922)
  mad_mob_data <- filter(mad_mob_data, 2807900 < mad_mob_data$destino)
  mad_mob_data <- filter(mad_mob_data, mad_mob_data$destino < 2807922)
  
  # Create travel matrix for the data and fill it up
  number_of_districts = 21
  travel_matrix<-matrix(0, nrow=number_of_districts, ncol=number_of_districts)

  for (i in 1:number_of_districts) {
    ii = 2807900 + i
    for (j in 1:number_of_districts) {
      jj = 2807900 + j
      travel_matrix[i,j] <- sum(mad_mob_data[which(mad_mob_data[,2]==ii & 
                                                     mad_mob_data[,3]==jj),10])
    }
  }

  # Add to reference week matrix
  ref_week_travel_matrix <- ref_week_travel_matrix + travel_matrix 
}

# Averaged travels over days added
avg_ref_week_travel_matrix = ref_week_travel_matrix / L

# Finally, get a travel rate matrix from this
file_name3 = 'mad_ref_week_travel_matrix.csv'
full_name3 = paste(full_path, file_name3, sep="")
write.table(avg_ref_week_travel_matrix, file=full_name3, sep=",", row.names=F)
