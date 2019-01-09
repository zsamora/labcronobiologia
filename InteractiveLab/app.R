library(shiny)

ui <- fluidPage(
  
  # Titulo
  titlePanel("Laboratorio de Cronobiología y Sueños - Visualización del sueño"),

  # Sidebar Layout
  sidebarLayout(
    # Sidebar Panel for inputs
    sidebarPanel("Inputs"),
    # Main Panel for displaying outputs
    mainPanel("Output")
  )
)

server <- function(input, output) {
  
}

shinyApp(ui = ui, server = server)
