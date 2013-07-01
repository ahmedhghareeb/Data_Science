# Stores the array of years in a variable called Year
Year <- c(1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969)

# Stores the array of populations in a variable called Population
Population <- c(4835, 4970, 5085, 5160, 5310, 5260, 5235, 5255, 5235, 5210, 5175)

#creates a data frame from the Year and Population arrays
sample1 <- data.frame(Year, Population)

#outputs the data frame
sample1

# Subtracts 1964 from every item in the Year column of the sample1 data frame
sample1$Year <- sample1$Year - 1964

#outputs the data frame
sample1

# plots the data from the sample1 data frame
plot(sample1$Year, sample1$Population, type="b")


# Create a linear model based on simple linear regression
fit1 <- lm(sample1$Population ~ sample1$Year)

# Create a linear model based on quadratic regression
fit2 <- lm(sample1$Population ~ sample1$Year + I(sample1$Year^2))

# Create a linear model based on cubic regression
fit3 <- lm(sample1$Population ~ sample1$Year + I(sample1$Year^2) + I(sample1$Year^3))

# Pay particular attention to this one!
fit4 <- lm(sample1$Population ~ sample1$Year + I(sample1$Year^3))

# Show summary tables for each of the linear models
summary(fit2)
summary(fit3)
summary(fit4)

# Plot the data and the linear models
plot(sample1$Year, sample1$Population, type="l", lwd=3)
points(sample1$Year, predict(fit2), type="l", col="red", lwd=2)
points(sample1$Year, predict(fit3), type="l", col="blue", lwd=2)
points(sample1$Year, predict(fit4), type="l", col="green", lwd=2)

# what is going on with fit4? Can you explain why it looks so different from fit2 and fit3?
# fit4 is taking fit3 and forcing the coeffecient of the Year^2 term to be 0. We are trying to force a quadratic model into a cubic function.
