# Librerias
library(imager)

# Variables globales
bright <- 0.25
contr <- 0.5
gamma <- 0.7
blur <- 5
sigma_filter <- 5 # Filtro gaussiano
size_filter <- 31 # ""

# Grayscale, filtering (low pass [blur] y high pass [edge detection]) y tresholding
transformImage <- function(img) {
  ##### Pre-procesamiento de la imagen
  ## Escala de grises
  img <- grayscale(img)
  #plot(img)
  ## Blur
  img <- isoblur(img,blur)
  #plot(img)
  ## Blur anisotropico
  #img <- blur_anisotropic(img, ampl=1e4,sharp=.3)
  ## Histogram equalisation
  #f <- ecdf(img)
  #img <-f(img) %>% as.cimg(dim=dim(img))
  ##### Alternativas
  ## Canny Edges (tiene mas opciones para modificar)
  img <- cannyEdges(img)
  #plot(img)
  ## Con magnitud de la gradiente
  #img <- imgradient(img,"xy") %>% enorm %>% cannyEdges
  #plot(img)
  ## Blur + deteccion de bordes + Sobel Edges
  #img <- deriche(img,2,order=2,axis="x") %>% deriche(2,order=2,axis="y")
  ## Segunda derivada (Laplacian of Gaussian)
  ## Con la funcion edge_detection (No funciona)
  #img <- edge_detection(img, method = 'Frei_chen')
  return (img)
}

centerMass <- function(img) {
  x <- 0
  y <- 0
  values <- which(img)
  for (v in values) {
    y <- y + floor(v / dim(img)[1])
    x <- x + (v - (floor(v / dim(img)[1]) * dim(img)[1]))
  }
  x <- x / length(values)
  y <- y / length(values)
  return(list("x" = x, "y" = y))
}

adjustFeatures <- function(img){
  # Brillo
  img <- img + bright
  # Contraste
  img <- img * contr
  # Gamma Correction
  img <- img ^ gamma
  return (img)
}

# Importar los archivos del experimento
experiment <- "/home/zsamora/Descargas/labcronobiologia/Experimento_12"
folders <- list.dirs(experiment, full.names = TRUE)
# Matriz vacia
dist_matrix <- matrix(nrow=length(folders), ncol=3600)
# Imagenes y centros de masa
arena <- NULL
img1 <- NULL
img2 <- NULL
res1 <- NULL
res2 <- NULL
# Variables
dist_tot <- 0
i <- 0
f <- 0
MIN <- 0
SEG <- -1

start.time <- Sys.time()
for (f in 2:2) {
  files <- list.files(path=folders[f], pattern="*.jpg", full.names = TRUE)
  for (i in 1:length(files)) {
    print(files[i])
    # Tiempo de la foto
    min = as.numeric(substr(strsplit(files[i],"/")[[1]][8],13,14))
    seg = as.numeric(substr(strsplit(files[i],"/")[[1]][8],15,16))
    # Si no es la primera foto, se guarda la foto anterior
    if (SEG != -1) {
      img1 <- img2
      res1 <- res2
    }
    # Carga de imagen en img2
    img2 <- load.image(files[i])
    # Seleccionar arena si es primera foto
    if (SEG == -1) { arena <- grabRect(as.array(img2))  }
    # Ajustes de imagen
    img2 <- imsub(img2, x >= arena[1], y >= arena[2]) %>% imsub(x <= (arena[3]-arena[1]), y <= (arena[4]-arena[2]))
    img2 <- adjustFeatures(img2)
    img2 <- transformImage(img2)
    res2 <- centerMass(img2)
    # Foto actual no es la foto esperada
    if (min != MIN || seg != SEG) {
      # Setea en NA la distancia de los segundos perdidos
      for (s in (60*MIN + SEG + 1):(60*min + seg + 1)) {
        dist_matrix[(f-1),s] <- NA  
      }
    }
    # Calculo de distancia (si existe foto anterior)
    if (SEG != -1) {
      dist <- sqrt((res2$y-res1$y)**2+(res2$x-res1$x)**2)
      dist_tot <- dist_tot + dist
      dist_matrix[(f-1),(60*min + seg + 1)] <- dist
      # Ploteo de imagen final
      imgfinal <- abs(img1/2 + img2)
      imgfinal[round(res1$x),round(res1$y)] <- 1
      imgfinal[round(res2$x),round(res2$y)] <- 1
      plot(imgfinal) 
    }
    # Foto inicial, setea la distancia en 0
    else {
      dist_matrix[(f-1),1] <- 0
      SEG <- 0
    }
    # Aumentar el tiempo de la foto esperada
    if (seg == 59) {
      MIN <- (min + 1) %% 60  
    }
    else {
      MIN <- min
    }
    SEG <- (seg + 1) %% 60
  }
}
end.time <- Sys.time()
time.taken <- end.time - start.time
time.taken
dist_tot
