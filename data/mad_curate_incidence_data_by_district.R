library("dplyr")
library("ggplot2")
library("patchwork")

# Prepare paths
new_wd = '/Users/ademiguel/workshop'
lower_path = '/citymob/data/'
folder_path = paste(new_wd, lower_path, sep="")

# Read csv as dataframe
file_name = 'modmad_covid19_tia_muni_y_distritos_s.csv'
full_name = paste(folder_path, file_name, sep="")
full_inc_df <- read.csv(full_name, header = TRUE, sep = ",")
renamed_cols = c('distrito', 'fecha', 'conf_ult_14d', 'tia_ult_14d', 'cas_conf_tot', 'tia_tot')
colnames(full_inc_df) <- renamed_cols 

# Extract Community of Madrid's municipios and distritos
com_madrid_zones = unique(full_inc_df[c("distrito")])$distrito
# Extract City of Madrid's distritos
madrid_districts = com_madrid_zones[-(22:length(com_madrid_zones))]

# Create new empty dataframe
or_inc_df <- data.frame(matrix(ncol = 6, nrow = 0))
colnames(or_inc_df) <- renamed_cols

# Fill dataframe with filtered data from Madrid districts
j = 1
for(i in 1:nrow(full_inc_df)) {       # for-loop over rows
  place_name = full_inc_df[i,1]
  if (place_name %in% madrid_districts) {
    or_inc_df[j,] = full_inc_df[i,]
    j = j + 1
  }
}

# Reverse row order
inc_df <- or_inc_df[dim(or_inc_df)[1]:1,]

# Get dates
full_date_length = length(inc_df$fecha)
date_col = vector()
for (i in 1:full_date_length)
{
  date_col[i] = substr(inc_df$fecha[i], 1, 10)
}
date_vector = unique(date_col)

# Create time series dataframe for observable 1: confirmed cases in last 14d
cc_last14d_df <- data.frame(matrix(ncol = 21, nrow = 0))
colnames(cc_last14d_df) <- madrid_districts
# Create time series dataframe for observable 2: TIA in last 14d
tia_last14d_df <- data.frame(matrix(ncol = 21, nrow = 0))
colnames(tia_last14d_df) <- madrid_districts
# Create time series dataframe for observable 3: confirmed cases in total
cc_total_df <- data.frame(matrix(ncol = 21, nrow = 0))
colnames(cc_total_df) <- madrid_districts
# Create time series dataframe for observable 2: TIA in total
tia_total_df <- data.frame(matrix(ncol = 21, nrow = 0))
colnames(tia_total_df) <- madrid_districts

# Fill the new dataframes from the common first dataframe
for (j in 1:length(madrid_districts)) {
  district = madrid_districts[j]
  k = 1
  for (i in 1:nrow(inc_df)) {
    if (inc_df[i,1] == district) {
      cc_last14d_df[k,j] = inc_df[i,3]
      tia_last14d_df[k,j] = inc_df[i,4]
      cc_total_df[k,j] = inc_df[i,5]
      tia_total_df[k,j] = inc_df[i,6]
      k = k + 1
    } 
  }
}

# Add date vector to dataframes
cc_last14d_df['date'] <- date_vector
tia_last14d_df['date'] <- date_vector
cc_total_df['date'] <- date_vector
tia_total_df['date'] <- date_vector

# Add an 'x'-axis variable (time)
cc_last14d_df['x'] <- 1:nrow(cc_last14d_df)
tia_last14d_df['x'] <- 1:nrow(tia_last14d_df)
cc_total_df['x'] <- 1:nrow(cc_total_df)
tia_total_df['x'] <- 1:nrow(tia_total_df)
# Get the time span (in weeks)
time_length = length(1:nrow(cc_last14d_df))

# Rename the new dataframes' columns more properly
new_names <- c('RETI', 'SALA', 'CENT', 'ARGA', 'CHMA', 'TETU', 'CHMB', 'FUEN', 
               'MONC', 'LATI', 'CARA', 'USER', 'PDVA', 'SBLA', 'BARA', 'MORA', 
               'CILI', 'HORT', 'VILL', 'VDVA', 'VICA', 'date', 'x')
colnames(cc_last14d_df) <- new_names
colnames(tia_last14d_df) <- new_names
colnames(cc_total_df) <- new_names
colnames(tia_total_df) <- new_names

write.csv(tia_last14d_df,'mad_tia_last14d_district.csv')

# 1st round of plotting: Confirmed cases in last 14 days (part I)
data_ggp <- data.frame(x = cc_last14d_df$x,                            # Reshape data frame
                       y = c(cc_last14d_df$RETI, 
                             cc_last14d_df$SALA, 
                             cc_last14d_df$CENT,
                             cc_last14d_df$ARGA,
                             cc_last14d_df$CHMA,
                             cc_last14d_df$TETU,
                             cc_last14d_df$CHMB,
                             cc_last14d_df$FUEN,
                             cc_last14d_df$MONC,
                             cc_last14d_df$LATI,
                             cc_last14d_df$CARA),
                       group = c(rep("RETI", nrow(cc_last14d_df)),
                                 rep("SALA", nrow(cc_last14d_df)),
                                 rep("CENT", nrow(cc_last14d_df)),
                                 rep("ARGA", nrow(cc_last14d_df)),
                                 rep("CHMA", nrow(cc_last14d_df)),
                                 rep("TETU", nrow(cc_last14d_df)),
                                 rep("CHMB", nrow(cc_last14d_df)),
                                 rep("FUEN", nrow(cc_last14d_df)),
                                 rep("MONC", nrow(cc_last14d_df)),
                                 rep("LATI", nrow(cc_last14d_df)),
                                 rep("CARA", nrow(cc_last14d_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp <- ggp+labs(x="weeks",y="14d-Confirmed cases",
                title="Time evolution for some districts (part I)")
ggp + facet_grid(group ~ .) + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed')

# 2nd round of plotting: Confirmed cases in last 14 days (part II)
data_ggp <- data.frame(x = cc_last14d_df$x,                            # Reshape data frame
                       y = c(cc_last14d_df$USER, 
                             cc_last14d_df$PDVA, 
                             cc_last14d_df$SBLA,
                             cc_last14d_df$BARA,
                             cc_last14d_df$MORA,
                             cc_last14d_df$CILI,
                             cc_last14d_df$HORT,
                             cc_last14d_df$VILL,
                             cc_last14d_df$VDVA,
                             cc_last14d_df$VICA,
                             cc_last14d_df$CENT),
                       group = c(rep("USER", nrow(cc_last14d_df)),
                                 rep("PDVA", nrow(cc_last14d_df)),
                                 rep("SBLA", nrow(cc_last14d_df)),
                                 rep("BARA", nrow(cc_last14d_df)),
                                 rep("MORA", nrow(cc_last14d_df)),
                                 rep("CILI", nrow(cc_last14d_df)),
                                 rep("HORT", nrow(cc_last14d_df)),
                                 rep("VILL", nrow(cc_last14d_df)),
                                 rep("VDVA", nrow(cc_last14d_df)),
                                 rep("VICA", nrow(cc_last14d_df)),
                                 rep("CENT", nrow(cc_last14d_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp <- ggp+labs(x="weeks",y="14d-Confirmed cases",
                title="Time evolution for some districts (part II)")
ggp + facet_grid(group ~ .) + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed')

# Invaded districts above confirmed cases in last 14d thresholds
incidence_threshold = c(100, 250, 500, 1000, 1500)
threshold_length = length(incidence_threshold)
inv_cclast14d_tseries_df <-as.data.frame(matrix(nrow=time_length, ncol=threshold_length))
character_vector <- as.character(incidence_threshold)
colnames(inv_cclast14d_tseries_df) <- character_vector

for (j in 1:ncol(inv_cclast14d_tseries_df)) {
  for (i in 1:nrow(inv_cclast14d_tseries_df)) {
    inv_cclast14d_tseries_df[i,j] = 0
  }
}

# Add an 'x'-axis variable (time)
inv_cclast14d_tseries_df['x'] <- 1:time_length

# Compute number of invaded districts under a certain incidence threshold
for(i in 1:time_length) {       # for-loop over time
  
  for(j in 1:ncol(cc_last14d_df)) { # for-loop over districts
    
    for(k in 1:threshold_length) { # for-loop over incidence thresholds
      if (!is.na(cc_last14d_df[i,j])){
        if (cc_last14d_df[i,j] >= incidence_threshold[k]) {
          inv_cclast14d_tseries_df[i,k] = inv_cclast14d_tseries_df[i,k] + 1
        }
      } 
    }
  }
}

# 3rd round of plotting: Invaded districts above confirmed cases in last 14d thresholds
data_ggp <- data.frame(x = inv_cclast14d_tseries_df$x,                            # Reshape data frame
                       y = c(inv_cclast14d_tseries_df$'250',
                             inv_cclast14d_tseries_df$'500',
                             inv_cclast14d_tseries_df$'1000',
                             inv_cclast14d_tseries_df$'1500'),
                       group = c(rep("0250", nrow(inv_cclast14d_tseries_df)),
                                 rep("0500", nrow(inv_cclast14d_tseries_df)),
                                 rep("1000", nrow(inv_cclast14d_tseries_df)),
                                 rep("1500", nrow(inv_cclast14d_tseries_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp + facet_grid(group ~ .) + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed')
ggp <- ggp+labs(x="weeks",y="invaded patches",
                title="14d-Confirmed Cases")
ggp + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed')

# 4th round of plotting: TIA in last 14d (part I)
data_ggp <- data.frame(x = tia_last14d_df$x,                            # Reshape data frame
                       y = c(tia_last14d_df$RETI, 
                             tia_last14d_df$SALA, 
                             tia_last14d_df$CENT,
                             tia_last14d_df$ARGA,
                             tia_last14d_df$CHMA,
                             tia_last14d_df$TETU,
                             tia_last14d_df$CHMB,
                             tia_last14d_df$FUEN,
                             tia_last14d_df$MONC,
                             tia_last14d_df$LATI,
                             tia_last14d_df$CARA),
                       group = c(rep("RETI", nrow(tia_last14d_df)),
                                 rep("SALA", nrow(tia_last14d_df)),
                                 rep("CENT", nrow(tia_last14d_df)),
                                 rep("ARGA", nrow(tia_last14d_df)),
                                 rep("CHMA", nrow(tia_last14d_df)),
                                 rep("TETU", nrow(tia_last14d_df)),
                                 rep("CHMB", nrow(tia_last14d_df)),
                                 rep("FUEN", nrow(tia_last14d_df)),
                                 rep("MONC", nrow(tia_last14d_df)),
                                 rep("LATI", nrow(tia_last14d_df)),
                                 rep("CARA", nrow(tia_last14d_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp <- ggp+labs(x="weeks",y="14d-Cumulative Incidence Rate",
                title="Time evolution for some districts (part I)")
ggp + facet_grid(group ~ .) + geom_hline(yintercept = 1000, color = 'black', linetype = 'dotted') + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') 

# 5th round of plotting: TIA in last 14d (part II)
data_ggp <- data.frame(x = tia_last14d_df$x,                            # Reshape data frame
                       y = c(tia_last14d_df$USER, 
                             tia_last14d_df$PDVA, 
                             tia_last14d_df$SBLA,
                             tia_last14d_df$BARA,
                             tia_last14d_df$MORA,
                             tia_last14d_df$CILI,
                             tia_last14d_df$HORT,
                             tia_last14d_df$VILL,
                             tia_last14d_df$VDVA,
                             tia_last14d_df$VICA,
                             tia_last14d_df$CENT),
                       group = c(rep("USER", nrow(tia_last14d_df)),
                                 rep("PDVA", nrow(tia_last14d_df)),
                                 rep("SBLA", nrow(tia_last14d_df)),
                                 rep("BARA", nrow(tia_last14d_df)),
                                 rep("MORA", nrow(tia_last14d_df)),
                                 rep("CILI", nrow(tia_last14d_df)),
                                 rep("HORT", nrow(tia_last14d_df)),
                                 rep("VILL", nrow(tia_last14d_df)),
                                 rep("VDVA", nrow(tia_last14d_df)),
                                 rep("VICA", nrow(tia_last14d_df)),
                                 rep("CENT", nrow(tia_last14d_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp <- ggp+labs(x="weeks",y="14d-Cumulative Incidence Rate",
                title="Time evolution for some districts (part II)")
ggp + facet_grid(group ~ .) + geom_hline(yintercept = 1000, color = 'black', linetype = 'dotted') + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') 

# Invaded districts above TIA in last 14d thresholds
incidence_threshold = c(100, 250, 500, 1000, 1500)
threshold_length = length(incidence_threshold)
inv_tialast14d_tseries_df <-as.data.frame(matrix(nrow=time_length, ncol=threshold_length))
character_vector <- as.character(incidence_threshold)
colnames(inv_tialast14d_tseries_df) <- character_vector

for (j in 1:ncol(inv_tialast14d_tseries_df)) {
  for (i in 1:nrow(inv_tialast14d_tseries_df)) {
    inv_tialast14d_tseries_df[i,j] = 0
  }
}

# Add an 'x'-axis variable (time)
inv_tialast14d_tseries_df['x'] <- 1:time_length

# Compute number of invaded districts under a certain incidence threshold
for(i in 1:time_length) {       # for-loop over time
  
  for(j in 1:ncol(tia_last14d_df)) { # for-loop over districts
    
    for(k in 1:threshold_length) { # for-loop over incidence thresholds
      if (!is.na(tia_last14d_df[i,j])){
        if (tia_last14d_df[i,j] >= incidence_threshold[k]) {
          inv_tialast14d_tseries_df[i,k] = inv_tialast14d_tseries_df[i,k] + 1
        }
      } 
    }
  }
}

# 6th round of plotting: Invaded districts above confirmed cases in last 14d thresholds
data_ggp <- data.frame(x = inv_tialast14d_tseries_df$x,                            # Reshape data frame
                       y = c(inv_tialast14d_tseries_df$'250',
                             inv_tialast14d_tseries_df$'500',
                             inv_tialast14d_tseries_df$'1000',
                             inv_tialast14d_tseries_df$'1500'),
                       group = c(rep("0250", nrow(inv_tialast14d_tseries_df)),
                                 rep("0500", nrow(inv_tialast14d_tseries_df)),
                                 rep("1000", nrow(inv_tialast14d_tseries_df)),
                                 rep("1500", nrow(inv_tialast14d_tseries_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp + facet_grid(group ~ .) + geom_hline(yintercept = 1000, color = 'black', linetype = 'dotted') + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') 
ggp <- ggp+labs(x="weeks",y="invaded patches",
                title="14d-Cumulative Incidence Rate")
ggp + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') 

