library("dplyr")
library("ggplot2")
library("patchwork")

# Prepare paths
new_wd = '/Users/ademiguel/workshop'
lower_path = '/perimetral/data/'
folder_path = paste(new_wd, lower_path, sep="")

# Read csv as dataframe
file_name = 'modmad_covid19_tia_zonas_basicas_salud_s.csv'
full_name = paste(folder_path, file_name, sep="")
full_inc_df <- read.csv(full_name, header = TRUE, sep = ",")
renamed_cols = c('zbs', 'fecha', 'conf_ult_14d', 'tia_ult_14d', 'cas_conf_tot', 'tia_tot')
colnames(full_inc_df) <- renamed_cols 

# Extract Comunidad de Madrid BHZs
com_madrid_zones = unique(full_inc_df[c("zbs")])$zbs
# Extract City of Madrid BHZs
madrid_bhz <- c('Puerta_Bonita', 'Vista_Alegre', 'Guayaba', 'Almendrales', 'Las_Calesas',
                'Zofío', 'Orcasur', 'San_Fermín', 'San_Andrés', 'San_Cristóbal', 'El_Espinillo',
                'Los_Rosales', 'Villa_Vallecas', 'Entrevías', 'San_Diego', 'Martínez_de_la_Riva',
                'Numancia', 'Peña_Prieta', 'Pozo_de_Tío_Raimundo', 'Ángela_Uriarte', 'Alcalá_de_Guadaíra',
                'Federica_Montseny', 'Doctor_Cirajas', 'Gandhi', 'Daroca', 'La_Elipa', 'Orcasitas',
                'Vicálvaro_Artilleros', 'Campo_de_la_Paloma', 'Rafael_Alberti', 'García_Noblejas',
                'Núñez_Morgado', 'Guzmán_el_Bueno', 'Vinateros_Torito', 'Pavones', 'Vandel',
                'Puerta_del_Ángel', 'Virgen_de_Begoña', 'Infanta_Mercedes', 'Villaamil',
                'Palma_Universidad', 'Eloy_Gonzalo', 'Justicia', 'Cortes', 'Cea_Bermúdez', 'Segovia',
                'Lavapiés', 'Alameda', 'Imperial', 'Acacias', 'Martín_de_Vargas', 'Embajadores',
                'Méndez_Álvaro', 'Legazpi', 'Chopera', 'Comillas', 'Antonio_Leyva',
                'Opañel', 'San_Isidro', 'Los_Cármenes', 'Lucero', 'General_Ricardos',
                'Abrantes', 'Los_Yébenes', 'Maqueda', 'Campamento', 'Buenavista', 'Las_Águilas',
                'Carabanchel_Alto', 'Butarque', 'Ensanche_Vallecas', 'Perales_del_Río',
                'Vicálvaro_Villablanca', 'Valdebernardo', 'Valderribas', 'Media_Legua', 'Estrella',
                'Adelfas', 'Pacífico', 'Ibiza', 'Castelló', 'Goya', 'General_Oráa', 'Montesa',
                'Londres', 'Espronceda', 'Segre', 'Prosperidad', 'Baviera', 'Canal_de_Panamá',
                'Estrecho_de_Corea', 'Aquitania', 'Simancas', 'Alpes', 'Quinta_de_los_Molinos', 
                'Silvano', 'Canillejas', 'Alameda_de_Osuna', 'Rejas', 'Benita_de_Ávila', 'Vicente_Muzas',
                'Potosí', 'General_Moscardó', 'Bustarviejo', 'Monovar', 'Jazmín', 'Mar_Báltico', 
                'Virgen_del_Cortijo', 'Sanchinarro', 'Las_Tablas', 'Pilar', 'La_Ventilla', 'Barajas',
                'Los_Alperchines', 'Mirasierra', 'Fuencarral', 'Montecarmelo', 'El_Pardo', 'Aravaca',
                'Valdezarza', 'Fuentelarreina', 'Casa_de_Campo', 'Argüelles', 'Andrés_Mellado',
                'Caramuel', 'General_Fanjul', 'Valle_Inclán', 'Alcocer', 'Portazgo', 'Barrio_del_Puerto',
                'Ciudad_de_los_Periodistas', 'Ciudad_San_Pablo', 'Doctor_Tamames', 'Los_Ángeles',
                'Monforte_de_Lemos', 'Peñagrande', 'Reina_Victoria', 'Santa_Eugenia', 'Valdeacederas')

# Create new empty dataframe
or_inc_df <- data.frame(matrix(ncol = 6, nrow = 0))
colnames(or_inc_df) <- renamed_cols

# Fill dataframe with filtered data from Madrid BHZs
j = 1
for(i in 1:nrow(full_inc_df)) {       # for-loop over rows
  place_name = full_inc_df[i,1]
  if (place_name %in% madrid_bhz) {
    or_inc_df[j,] = full_inc_df[i,]
    j = j + 1
  }
}

# Reverse row order
inc_df <- or_inc_df[dim(or_inc_df)[1]:1,]

# Create time series dataframe for observable 1: confirmed cases in last 14d
bhz_number = length(madrid_bhz)
cc_last14d_df <- data.frame(matrix(ncol = bhz_number, nrow = 0))
colnames(cc_last14d_df) <- madrid_bhz
# Create time series dataframe for observable 2: TIA in last 14d
tia_last14d_df <- data.frame(matrix(ncol = bhz_number, nrow = 0))
colnames(tia_last14d_df) <- madrid_bhz
# Create time series dataframe for observable 3: confirmed cases in total
cc_total_df <- data.frame(matrix(ncol = bhz_number, nrow = 0))
colnames(cc_total_df) <- madrid_bhz
# Create time series dataframe for observable 2: TIA in total
tia_total_df <- data.frame(matrix(ncol = bhz_number, nrow = 0))
colnames(tia_total_df) <- madrid_bhz

# Fill the new dataframes from the common first dataframe
for (j in 1:length(madrid_bhz)) {
  bhz = madrid_bhz[j]
  k = 1
  for (i in 1:nrow(inc_df)) {
    if (inc_df[i,1] == bhz) {
      cc_last14d_df[k,j] = inc_df[i,3]
      tia_last14d_df[k,j] = inc_df[i,4]
      cc_total_df[k,j] = inc_df[i,5]
      tia_total_df[k,j] = inc_df[i,6]
      k = k + 1
    } 
  }
}

# Add an 'x'-axis variable (time)
cc_last14d_df['x'] <- 1:nrow(cc_last14d_df)
tia_last14d_df['x'] <- 1:nrow(tia_last14d_df)
cc_total_df['x'] <- 1:nrow(cc_total_df)
tia_total_df['x'] <- 1:nrow(tia_total_df)
# Get the time span (in weeks)
time_length = length(1:nrow(cc_last14d_df))

# Save dataframe for LAST 14 DAY CIR into CSV file
write.csv(tia_last14d_df,'mad_tia_last14d_bhz.csv')

# 1st round of plotting: Confirmed cases in last 14 days (Confined BHZs)
data_ggp <- data.frame(x = cc_last14d_df$x,                            # Reshape data frame
                       y = c(cc_last14d_df$Puerta_Bonita, 
                             cc_last14d_df$Vista_Alegre,
                             cc_last14d_df$Guayaba,
                             cc_last14d_df$Almendrales,
                             cc_last14d_df$Las_Calesas,
                             cc_last14d_df$Zofío,
                             cc_last14d_df$Orcasur,
                             cc_last14d_df$San_Fermín,
                             cc_last14d_df$San_Andrés,
                             cc_last14d_df$San_Cristóbal,
                             cc_last14d_df$El_Espinillo,
                             cc_last14d_df$Los_Rosales,
                             cc_last14d_df$Villa_Vallecas,
                             cc_last14d_df$Entrevías,
                             cc_last14d_df$San_Diego,
                             cc_last14d_df$Martínez_de_la_Riva,
                             cc_last14d_df$Numancia,
                             cc_last14d_df$Peña_Prieta,
                             cc_last14d_df$Pozo_de_Tío_Raimundo,
                             cc_last14d_df$Ángela_Uriarte,
                             cc_last14d_df$Alcalá_de_Guadaíra,
                             cc_last14d_df$Federica_Montseny,
                             cc_last14d_df$Doctor_Cirajas,
                             cc_last14d_df$Gandhi,
                             cc_last14d_df$Daroca,
                             cc_last14d_df$La_Elipa,
                             cc_last14d_df$Orcasitas,
                             cc_last14d_df$Vicálvaro_Astilleros,
                             cc_last14d_df$Campo_de_la_Paloma,
                             cc_last14d_df$Rafael_Alberti,
                             cc_last14d_df$García_Noblejas,
                             cc_last14d_df$Núñez_Morgado,
                             cc_last14d_df$Guzmán_el_Bueno,
                             cc_last14d_df$Vinateros_Torito,
                             cc_last14d_df$Pavones,
                             cc_last14d_df$Vandel,
                             cc_last14d_df$Puerta_del_Ángel,
                             cc_last14d_df$Virgen_de_Begoña,
                             cc_last14d_df$Infanta_Mercedes,
                             cc_last14d_df$Villaamil),
                       group = c(rep("Puerta_Bonita", nrow(cc_last14d_df)),
                                 rep("Vista_Alegre", nrow(cc_last14d_df)),
                                 rep("Guayaba", nrow(cc_last14d_df)),
                                 rep("Almendrales", nrow(cc_last14d_df)),
                                 rep("Calesas", nrow(cc_last14d_df)),
                                 rep("Zofío", nrow(cc_last14d_df)),
                                 rep("Orcasur", nrow(cc_last14d_df)),
                                 rep("S_Fermin", nrow(cc_last14d_df)),
                                 rep("S_Andrés", nrow(cc_last14d_df)),
                                 rep("S_Cristóbal", nrow(cc_last14d_df)),
                                 rep("Espinillo", nrow(cc_last14d_df)),
                                 rep("Rosales", nrow(cc_last14d_df)),
                                 rep("Villa_Vallecas", nrow(cc_last14d_df)),
                                 rep("Entrevías", nrow(cc_last14d_df)),
                                 rep("S_Diego", nrow(cc_last14d_df)),
                                 rep("M_de_la_Riva", nrow(cc_last14d_df)),
                                 rep("Numancia", nrow(cc_last14d_df)),
                                 rep("Peña_Prieta", nrow(cc_last14d_df)),
                                 rep("Pozo_Tío_Rai", nrow(cc_last14d_df)),
                                 rep("Ángela_Uriarte", nrow(cc_last14d_df)),
                                 rep("Alcalá_Guadaíra", nrow(cc_last14d_df)),
                                 rep("Federica_Mont.", nrow(cc_last14d_df)),
                                 rep("Dr_Cirajas", nrow(cc_last14d_df)),
                                 rep("Gandhi", nrow(cc_last14d_df)),
                                 rep("Daroca", nrow(cc_last14d_df)),
                                 rep("La_Elipa", nrow(cc_last14d_df)),
                                 rep("Orcasitas", nrow(cc_last14d_df)),
                                 rep("Vicálvaro_Art.", nrow(cc_last14d_df)),
                                 rep("Campo_Paloma", nrow(cc_last14d_df)),
                                 rep("Rafael_Alberti", nrow(cc_last14d_df)),
                                 rep("García_Noblejas", nrow(cc_last14d_df)),
                                 rep("Núñez_Morgado", nrow(cc_last14d_df)),
                                 rep("Guzmán_el_Bueno", nrow(cc_last14d_df)),
                                 rep("Vinateros", nrow(cc_last14d_df)),
                                 rep("Pavones", nrow(cc_last14d_df)),
                                 rep("Vandel", nrow(cc_last14d_df)),
                                 rep("Puerta_Ángel", nrow(cc_last14d_df)),
                                 rep("Virgen_Begoña", nrow(cc_last14d_df)),
                                 rep("Infanta_Mer", nrow(cc_last14d_df)),
                                 rep("Villaamil", nrow(cc_last14d_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp <- ggp+labs(x="weeks",y="14d-Confirmed cases",
                title="Time evolution for confined BHZs")
ggp + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') + geom_vline(xintercept = 32, color = 'grey', linetype = 'dotted')#+ facet_grid(group ~ .)

# 2nd round of plotting: Confirmed cases in last 14 days (Selected free BHZs)
data_ggp <- data.frame(x = cc_last14d_df$x,                            # Reshape data frame
                       y = c(cc_last14d_df$Palma_Universidad, 
                             cc_last14d_df$Legazpi, 
                             cc_last14d_df$San_Isidro,
                             cc_last14d_df$Alameda,
                             cc_last14d_df$Lavapiés,
                             cc_last14d_df$Cortes,
                             cc_last14d_df$Carabanchel_Alto,
                             cc_last14d_df$Goya,
                             cc_last14d_df$Canal_de_Panamá,
                             cc_last14d_df$Espronceda,
                             cc_last14d_df$Potosí,
                             cc_last14d_df$General_Moscardó, 
                             cc_last14d_df$General_Fanjul, 
                             cc_last14d_df$Mar_Báltico,
                             cc_last14d_df$Sanchinarro,
                             cc_last14d_df$Pilar,
                             cc_last14d_df$Fuencarral,
                             cc_last14d_df$El_Pardo,
                             cc_last14d_df$Aravaca,
                             cc_last14d_df$Casa_de_Campo,
                             cc_last14d_df$Los_Cármenes,
                             cc_last14d_df$Valle_Inclán),
                       group = c(rep("Palma", nrow(cc_last14d_df)),
                                 rep("Legazpi", nrow(cc_last14d_df)),
                                 rep("S_Isidro", nrow(cc_last14d_df)),
                                 rep("Alameda", nrow(cc_last14d_df)),
                                 rep("Lavapiés", nrow(cc_last14d_df)),
                                 rep("Cortes", nrow(cc_last14d_df)),
                                 rep("Caraban_Alto", nrow(cc_last14d_df)),
                                 rep("Goya", nrow(cc_last14d_df)),
                                 rep("Canal_de_Panamá", nrow(cc_last14d_df)),
                                 rep("Espronceda", nrow(cc_last14d_df)),
                                 rep("Potosí", nrow(cc_last14d_df)),
                                 rep("G_Moscardó", nrow(cc_last14d_df)),
                                 rep("G_Fanjul", nrow(cc_last14d_df)),
                                 rep("Mar_Báltico", nrow(cc_last14d_df)),
                                 rep("Sanchinarro", nrow(cc_last14d_df)),
                                 rep("Pilar", nrow(cc_last14d_df)),
                                 rep("Fuencarral", nrow(cc_last14d_df)),
                                 rep("El_Pardo", nrow(cc_last14d_df)),
                                 rep("Aravaca", nrow(cc_last14d_df)),
                                 rep("Casa_de_Campo", nrow(cc_last14d_df)),
                                 rep("Los_Cármenes", nrow(cc_last14d_df)),
                                 rep("Valle_Inclán", nrow(cc_last14d_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp <- ggp+labs(x="weeks",y="14d-Confirmed cases",
                title="Time evolution for selected free BHZs")
ggp + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') + geom_vline(xintercept = 32, color = 'grey', linetype = 'dotted')#+ facet_grid(group ~ .)#+ facet_grid(group ~ .)

# Invaded districts above confirmed cases in last 14d thresholds
incidence_threshold = c(50, 100, 250, 400, 500)
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
                       y = c(inv_cclast14d_tseries_df$'50',
                             inv_cclast14d_tseries_df$'100',
                             inv_cclast14d_tseries_df$'250',
                             inv_cclast14d_tseries_df$'400'),
                       group = c(rep("050", nrow(inv_cclast14d_tseries_df)),
                                 rep("100", nrow(inv_cclast14d_tseries_df)),
                                 rep("250", nrow(inv_cclast14d_tseries_df)),
                                 rep("400", nrow(inv_cclast14d_tseries_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp + facet_grid(group ~ .)
ggp <- ggp+labs(x="weeks",y="invaded patches",
                title="14d-Confirmed Cases")
ggp + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') + geom_vline(xintercept = 32, color = 'grey', linetype = 'dotted')#+ facet_grid(group ~ .)

# 4th round of plotting: TIA in last 14d (confined BHZs)
data_ggp <- data.frame(x = tia_last14d_df$x,                            # Reshape data frame
                       y = c(tia_last14d_df$Puerta_Bonita, 
                             tia_last14d_df$Vista_Alegre,
                             tia_last14d_df$Guayaba,
                             tia_last14d_df$Almendrales,
                             tia_last14d_df$Las_Calesas,
                             tia_last14d_df$Zofío,
                             tia_last14d_df$Orcasur,
                             tia_last14d_df$San_Fermín,
                             tia_last14d_df$San_Andrés,
                             tia_last14d_df$San_Cristóbal,
                             tia_last14d_df$El_Espinillo,
                             tia_last14d_df$Los_Rosales,
                             tia_last14d_df$Villa_Vallecas,
                             tia_last14d_df$Entrevías,
                             tia_last14d_df$San_Diego,
                             tia_last14d_df$Martínez_de_la_Riva,
                             tia_last14d_df$Numancia,
                             tia_last14d_df$Peña_Prieta,
                             tia_last14d_df$Pozo_de_Tío_Raimundo,
                             tia_last14d_df$Ángela_Uriarte,
                             tia_last14d_df$Alcalá_de_Guadaíra,
                             tia_last14d_df$Federica_Montseny,
                             tia_last14d_df$Doctor_Cirajas,
                             tia_last14d_df$Gandhi,
                             tia_last14d_df$Daroca,
                             tia_last14d_df$La_Elipa,
                             tia_last14d_df$Orcasitas,
                             tia_last14d_df$Vicálvaro_Artilleros,
                             tia_last14d_df$Campo_de_la_Paloma,
                             tia_last14d_df$Rafael_Alberti,
                             tia_last14d_df$García_Noblejas,
                             tia_last14d_df$Núñez_Morgado,
                             tia_last14d_df$Guzmán_el_Bueno,
                             tia_last14d_df$Vinateros_Torito,
                             tia_last14d_df$Pavones,
                             tia_last14d_df$Vandel,
                             tia_last14d_df$Puerta_del_Ángel,
                             tia_last14d_df$Virgen_de_Begoña,
                             tia_last14d_df$Infanta_Mercedes,
                             tia_last14d_df$Villaamil),
                       group = c(rep("Puerta_Bonita", nrow(tia_last14d_df)),
                                 rep("Vista_Alegre", nrow(tia_last14d_df)),
                                 rep("Guayaba", nrow(tia_last14d_df)),
                                 rep("Almendrales", nrow(tia_last14d_df)),
                                 rep("Calesas", nrow(tia_last14d_df)),
                                 rep("Zofío", nrow(tia_last14d_df)),
                                 rep("Orcasur", nrow(tia_last14d_df)),
                                 rep("S_Fermin", nrow(tia_last14d_df)),
                                 rep("S_Andrés", nrow(tia_last14d_df)),
                                 rep("S_Cristóbal", nrow(tia_last14d_df)),
                                 rep("Espinillo", nrow(tia_last14d_df)),
                                 rep("Rosales", nrow(tia_last14d_df)),
                                 rep("Villa_Vallecas", nrow(tia_last14d_df)),
                                 rep("Entrevías", nrow(tia_last14d_df)),
                                 rep("S_Diego", nrow(tia_last14d_df)),
                                 rep("M_de_la_Riva", nrow(tia_last14d_df)),
                                 rep("Numancia", nrow(tia_last14d_df)),
                                 rep("Peña_Prieta", nrow(tia_last14d_df)),
                                 rep("Pozo_Tío_Rai", nrow(tia_last14d_df)),
                                 rep("Ángela_Uriarte", nrow(tia_last14d_df)),
                                 rep("Alcalá_Guadaíra", nrow(tia_last14d_df)),
                                 rep("Federica_Mont.", nrow(tia_last14d_df)),
                                 rep("Dr_Cirajas", nrow(tia_last14d_df)),
                                 rep("Gandhi", nrow(tia_last14d_df)),
                                 rep("Daroca", nrow(tia_last14d_df)),
                                 rep("La_Elipa", nrow(tia_last14d_df)),
                                 rep("Orcasitas", nrow(tia_last14d_df)),
                                 rep("Vicálvaro_Ast.", nrow(tia_last14d_df)),
                                 rep("Campo_Paloma", nrow(tia_last14d_df)),
                                 rep("Rafael_Alberti", nrow(tia_last14d_df)),
                                 rep("García_Noblejas", nrow(tia_last14d_df)),
                                 rep("Núñez_Morgado", nrow(tia_last14d_df)),
                                 rep("Guzmán_el_Bueno", nrow(tia_last14d_df)),
                                 rep("Vinateros", nrow(tia_last14d_df)),
                                 rep("Pavones", nrow(tia_last14d_df)),
                                 rep("Vandel", nrow(tia_last14d_df)),
                                 rep("Puerta_Ángel", nrow(tia_last14d_df)),
                                 rep("Virgen_Begoña", nrow(tia_last14d_df)),
                                 rep("Infanta_Mer", nrow(tia_last14d_df)),
                                 rep("Villaamil", nrow(tia_last14d_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp <- ggp+labs(x="weeks",y="14d-Cumulative Incidence Rate",
                title="Time evolution for confined BHZs")
ggp + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') + geom_vline(xintercept = 32, color = 'grey', linetype = 'dotted')#+ facet_grid(group ~ .)

# 5th round of plotting: TIA in last 14d (selected free BHZs)
data_ggp <- data.frame(x = tia_last14d_df$x,                            # Reshape data frame
                       y = c(tia_last14d_df$Palma_Universidad, 
                             tia_last14d_df$Legazpi, 
                             tia_last14d_df$San_Isidro,
                             tia_last14d_df$Alameda,
                             tia_last14d_df$Lavapiés,
                             tia_last14d_df$Cortes,
                             tia_last14d_df$Carabanchel_Alto,
                             tia_last14d_df$Goya,
                             tia_last14d_df$Canal_de_Panamá,
                             tia_last14d_df$Espronceda,
                             tia_last14d_df$Potosí,
                             tia_last14d_df$General_Moscardó, 
                             tia_last14d_df$General_Fanjul, 
                             tia_last14d_df$Mar_Báltico,
                             tia_last14d_df$Sanchinarro,
                             tia_last14d_df$Pilar,
                             tia_last14d_df$Fuencarral,
                             tia_last14d_df$El_Pardo,
                             tia_last14d_df$Aravaca,
                             tia_last14d_df$Casa_de_Campo,
                             tia_last14d_df$Los_Cármenes,
                             tia_last14d_df$Valle_Inclán),
                       group = c(rep("Palma", nrow(tia_last14d_df)),
                                 rep("Legazpi", nrow(tia_last14d_df)),
                                 rep("S_Isidro", nrow(tia_last14d_df)),
                                 rep("Alameda", nrow(tia_last14d_df)),
                                 rep("Lavapiés", nrow(tia_last14d_df)),
                                 rep("Cortes", nrow(tia_last14d_df)),
                                 rep("Caraban_Alto", nrow(tia_last14d_df)),
                                 rep("Goya", nrow(tia_last14d_df)),
                                 rep("Canal_de_Panamá", nrow(tia_last14d_df)),
                                 rep("Espronceda", nrow(tia_last14d_df)),
                                 rep("Potosí", nrow(tia_last14d_df)),
                                 rep("G_Moscardó", nrow(tia_last14d_df)),
                                 rep("G_Fanjul", nrow(tia_last14d_df)),
                                 rep("Mar_Báltico", nrow(tia_last14d_df)),
                                 rep("Sanchinarro", nrow(tia_last14d_df)),
                                 rep("Pilar", nrow(tia_last14d_df)),
                                 rep("Fuencarral", nrow(tia_last14d_df)),
                                 rep("El_Pardo", nrow(tia_last14d_df)),
                                 rep("Aravaca", nrow(tia_last14d_df)),
                                 rep("Casa_de_Campo", nrow(tia_last14d_df)),
                                 rep("Los_Cármenes", nrow(tia_last14d_df)),
                                 rep("Valle_Inclán", nrow(tia_last14d_df))))

ggp <- ggplot(data_ggp, aes(x, y, col = group)) + geom_line()
ggp <- ggp+labs(x="weeks",y="114d-Cumulative Incidence Rate",
                title="Time evolution for selected free BHZs")
ggp + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') + geom_vline(xintercept = 32, color = 'grey', linetype = 'dotted')#+ facet_grid(group ~ .)

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
ggp + facet_grid(group ~ .)
ggp <- ggp+labs(x="weeks",y="invaded patches",
                title="14d-Cumulative Incidence Rate")
ggp + geom_vline(xintercept = 18, color = 'red', linetype = 'dashed') + geom_vline(xintercept = 32, color = 'grey', linetype = 'dotted')#+ facet_grid(group ~ .)

