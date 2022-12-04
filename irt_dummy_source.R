# install.packages("TAM")
library(TAM)

data("data.melab")

examen <- data.melab$data

modelo   <- tam.mml(examen)
personas <- tam.wle(modelo)

theta  = (personas$theta * 10) + 50
error  = sqrt((personas$error * 10))
scores = data.frame(theta, error) 

write.csv(scores, file = "irt_dummy.csv", row.names = FALSE)
