library(chron)
library(zoo)
library(xts)

zoo.data <- read.zoo(
                "metric-data.txt",
                FUN = function(x) { as.chron(as.vector(x)) },
                sep="\t",
                header=TRUE,
                colClasses=c("character", "character", "numeric")
                )
zoo.data$value <- as.numeric(zoo.data$value)
xts.data <- as.xts(zoo.data)

pdf("plot.png")
plot(xts.data, type='b')
dev.off()
