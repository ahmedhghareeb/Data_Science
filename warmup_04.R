# Installs the packages for DMwR
install.packages('DMwR')

# Loads the library into this R session
library(DMwR)

# Loads the algae data set
data(algae)

# Prints a summary table of the algae data set
summary(algae)

# Displays a histogram
hist(algae$mxPH, prob = T)

# Plots
plot(algae$NH4, xlab = '')
abline(h = mean(algae$NH4, na.rm = T), lty = 1)
abline(h = mean(algae$NH4, na.rm = T) + sd(algae$NH4, na.rm = T), lty = 2)
abline(h = median(algae$NH4, na.rm = T), lty = 3)

lm(PO4 ~ oPO4, data = algae)
clean.algae <- knnImputation(algae, k = 10)

lm.a1 <- lm(a1 ~ ., data = clean.algae[, 1:12])
summary(lm.a1)
anova(lm.a1)

lm2.a1 <- update(lm.a1, . ~ . - season)
summary(lm2.a1)
anova(lm.a1, lm2.a1)

final.lm <- step(lm.a1)
