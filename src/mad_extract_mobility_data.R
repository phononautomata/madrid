# This script collects all the daily raw data involving travels within the
# districts of the city of Madrid, Spain, during several months of the period 
# 2020-2021. 

# In order for the script to work properly, the raw data from the
# Ministry of Transport has to be stored where the lower_path says.

# The output of this script is a csv file for every single day from which the
# raw data was obtained. The csv file is a 21 x 21 table, where every element 
# (ij) represents the total number of travels that took place in that date 
# between districts i and j according to the raw data.

library("dplyr")

path <- setwd("~/madrid")
lower_path <- 'data/daily_maestra1_mitma_distrito/'
full_path <- file.path(path, lower_path)

#folder_path = paste(new_wd, lower_path, sep="")

file_name_ending = '_maestra_1_mitma_distrito'

day_list = c('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
            '31')
month_list = c('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
              '11', '12')
year_list = c('2020', '2021')

for (year in year_list) {
  for (month in month_list) {
    for (day in day_list) {
      
      # Paste full date string
      full_date = paste(year, month, day, sep="")
      
      # Build full file name
      full_name = paste(full_path, full_date, file_name_ending, ".txt", 
                        sep="")
      
      if (file.exists(full_name)) {
        
        print(full_date)
        
        # Read txt file and replace symbols
        tx <- readLines(full_name)
        tx2 <- gsub(pattern ="|", replace = ",", x = tx, fixed = TRUE)
        
        writeLines(tx2, con=full_name2)
        
        # Read csv as dataframe, check variable type
        mob_data <- read.csv(full_name2, header = TRUE, sep = ",")
        
        # Change 'origen' & 'destino' columns from character to numeric
        i <- c(2, 3)
        mob_data[ , i] <- apply(mob_data[ , i], 2, 
                                function(x) as.numeric(as.character(x)))
        
        # Filter travels within city districts 
        # MAD: CPRO=28, CMUN=079, CSEC=01 to 21
        CPRO = 28
        CMUN = 079

        city_mob_data <- filter(mob_data, 2807900 < mob_data$origen)
        city_mob_data <- filter(city_mob_data, city_mob_data$origen < 2807922)
        city_mob_data <- filter(city_mob_data, 2807900 < city_mob_data$destino)
        city_mob_data <- filter(city_mob_data, city_mob_data$destino < 2807922)
        
        # Create travel matrix for the data and fill it up
        number_of_districts = 21
        travel_matrix <- matrix(0, nrow=number_of_districts, 
                                ncol=number_of_districts)
        
        for (i in 1:number_of_districts) {
          ii = 2807900 + i
          for (j in 1:number_of_districts) {
            jj = 2807900 + j
            travel_matrix[i,j] <- sum(city_mob_data[which(city_mob_data[,2]==ii 
                                                          & city_mob_data[,3]==jj),10])
          }
        }
        
        # Write travel matrix to file
        prefix_name = 'mad_travel_matrix_'
        full_name = paste(full_path, prefix_name, full_date, '.csv', sep="")
        write.table(travel_matrix, file=full_name, sep=",", row.names=F)
      }
    }
  }
}
