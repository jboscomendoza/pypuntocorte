# install.packages("TAM")
library(TAM)


# Datos incluidos en TAM
data("data.melab")
examen <- data.melab$data


# Parametros de los items
modelo   <- tam.mml(examen)

items <- modelo$xsi
items <- items * 10
names(items) <- c("b", "error")

items$b  <- items$b + 50
items$id <- row.names(modelo$xsi)


# Parametros de las personas
personas <- tam.wle(modelo)

theta  <- (personas$theta * 10) + 50
error  <- sqrt((personas$error * 10))
scores <- data.frame(theta, error)


# Exportar a csv
write.csv(scores, file = "irt_dummy.csv", row.names = FALSE)
write.csv(items, file = "irt_items.csv", row.names = FALSE)
