# install.packages("TAM")
library(TAM)

data("data.melab")

examen <- data.melab$data

modelo   <- tam.mml(examen)
personas <- tam.wle(modelo)

items = modelo$xsi
items = items * 10
items$b = items$b + 50
names(items) = c("b", "error")
items$id = row.names(modelo$xsi)

theta  = (personas$theta * 10) + 50
error  = sqrt((personas$error * 10))
scores = data.frame(theta, error) 

write.csv(scores, file = "irt_dummy.csv", row.names = FALSE)
write.csv(items, file = "irt_items.csv", row.names = FALSE)
