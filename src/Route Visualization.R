install.packages("googleway")
install.packages("leaflet")
install.packages("magrittr")
install.packages("RColorBrewer")
install.packages("osrm")

library(googleway)
library(leaflet)
library(magrittr)
library(RColorBrewer)
library(osrm)


# 고정형 충전소 아이콘
EVcharger <- makeIcon(
  iconUrl = "https://cdn-icons-png.flaticon.com/512/7512/7512281.png",
  iconWidth = 30, iconHeight = 30,
)

# 이동형 충전소 아이콘
EVcharger_move <- makeIcon(
  iconUrl = "https://cdn-icons-png.flaticon.com/512/5615/5615874.png",
  iconWidth = 20, iconHeight = 20,
)

LabelYes <- TRUE

Schedule <- read.csv('dist_ny_sim3.csv')
Vehicles <- as.vector(Schedule$VID)


Vehicles <- unique(Vehicles)


Vehicles <- sort(Vehicles)

ColSets <- brewer.pal(n = 8, name = "Dark2")

MapResult <- leaflet() %>%
  addProviderTiles(providers$CartoDB.Positron)

for (vid in Vehicles) {
  Focused <- subset(Schedule, VID == vid) # subset(데이터, 조건) : 데이터 중 조건에 맞는 것만 추출
  First <- head(Focused, 1)
  Last <- tail(Focused, 1)
  
  if (Focused$Task_Type[1] == "Fixed") { # 고정형
    for (row in 1:(nrow(Focused))) {
      waypt <- c()
      waypt[[1]] <- c(0, Focused[row, "From_Lon"], Focused[row, "From_Lat"])
      waypt[[2]] <- c(1, Focused[row, "To_Lon"], Focused[row, "To_Lat"])
      
      df <- do.call(rbind.data.frame, waypt) # do.call(함수, 대상): 함수를 대상에 반복적으로 적용
      colnames(df)[1] <- "com"
      colnames(df)[2] <- "lon"
      colnames(df)[3] <- "lat"
      
      trips <-osrmRoute(loc = df, overview = "full",returnclass="sf", osrm.profile = "car" )
      
      # 선 삽입
      MapResult <-
        addPolylines(map = MapResult, data = trips, color = ColSets[vid+1])
      
      # 충전소 위치 삽입
      MapResult <-
        addMarkers(map = MapResult, lat = Focused[row, "To_Lat"],
                   lng = Focused[row, "To_Lon"], icon = EVcharger)
      
      # 전기차 출발 위치 삽입
      MapResult <-
        addCircleMarkers(map = MapResult, lat = Focused[row, "From_Lat"],
                         lng = Focused[row, "From_Lon"],
                         color = ColSets[vid+1],
                         stroke = FALSE,
                         radius = 5,
                         fillOpacity = 1
        )
      
    }
    
  } else { # 이동형
    waypt <- c() 
    waypt[[1]] <- c(0, First$From_Lon, First$From_Lat)
    i = 2
    for (row in 1:(nrow(Focused))) {
      via = c(row, Focused[row, "To_Lon"], Focused[row, "To_Lat"])
      waypt[[i]] <- via
      i = i + 1
    }
    
    df <- do.call(rbind.data.frame, waypt) # do.call(함수, 대상): 함수를 대상에 반복적으로 적용
    colnames(df)[1] <- "com"
    colnames(df)[2] <- "lon"
    colnames(df)[3] <- "lat"
    
    trips <- osrmRoute(loc = df, overview = "full", returnclass="sf", osrm.profile = "car")
    
    # 선 삽입
    MapResult <-
      addPolylines(map = MapResult, data = trips, color = ColSets[vid+1])
    
    # 이동형 충전소 출발 위치 삽입
    MapResult <-
      addMarkers(map = MapResult, lat = First$From_Lat,
                 First$From_Lon, icon = EVcharger_move)
    
    # 전기차 위치 삽입
    for (row in 1:(nrow(Focused))) {
      MapResult <-
        addCircleMarkers(map = MapResult, lat = Focused[row, "To_Lat"],
                         lng = Focused[row, "To_Lon"],
                         color = ColSets[vid+1],
                         stroke = FALSE,
                         radius = 5,
                         fillOpacity = 1)
    }
    
  }
}


MapResult

