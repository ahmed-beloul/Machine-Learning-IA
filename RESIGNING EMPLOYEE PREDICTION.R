#import libraries
library(readr) #to read csv
library(Hmisc) #to describes dataframe
library(corrplot) #shows correlation between variables
library(ggcorrplot) #visualizes heatmap of correlation
library(ggplot2) #to visualize data using ggplot
library(stringr) #to change the column value
library(dplyr) #so we can use pipe and filter
library(Amelia) #missmap
library(rpart)
library(rpart.plot)
library(randomForest)
library(naivebayes)
library(caret)
library (e1071) #datapartition



#import dataset
Company <- read.csv("C:\\Users\\ahmed\\Downloads\\archive\\Employee.csv")

head(Company) 
summary(Company)
dim(Company)

#print unique string value
unique(Company$City)
unique(Company$Gender)
unique(Company$Education)
unique(Company$EverBenched)

#add new numeric column 
Company$City_num <- str_replace_all(Company$City, c('Bangalore'="0",'Pune'="1","New Delhi"="2" ))
Company$Gender_num <- str_replace_all(Company$Gender, c('Male'="0",'Female'="1"))
Company$Education_num <- str_replace_all(Company$Education, c('Bachelors'="0",'Masters'="1",'PHD'="2"))
Company$EverBenched_num <- str_replace_all(Company$EverBenched, c('No'="0",'Yes'="1"))

Company$City_num <- as.numeric(as.character(Company$City_num))  # Convert variable to numeric
Company$Gender_num <- as.numeric(as.character(Company$Gender_num))
Company$Education_num <- as.numeric(as.character(Company$Education_num))
Company$EverBenched_num <- as.numeric(as.character(Company$EverBenched_num))

Company$TimeinCompany <- 2018 - Company$JoiningYear



head(Company)

#verify missing data
missmap(Company)

ggplot(Company) +
  geom_density(aes(x=JoiningYear, color = City), size = 1) +
  labs(x = "Year of Join", title = "Joining Year of Employee of Every City")

#repartition graphs
ggplot(Company, aes(LeaveOrNot)) +
  geom_histogram(color="darkblue",
                 fill = 'lightblue')

#proportion leave/notleave 
PercentLeave <- Company %>% 
  group_by(LeaveOrNot) %>% 
  count() %>% 
  ungroup() %>% 
  mutate(perc = `n` / sum(`n`)) %>% 
  arrange(perc) %>%
  mutate(labels = scales::percent(perc))
View(PercentLeave)

#proportion femme/homme
PercentGender <- Company %>% 
  group_by(Gender) %>% 
  count() %>% 
  ungroup() %>% 
  mutate(perc = `n` / sum(`n`)) %>% 
  arrange(perc) %>%
  mutate(labels = scales::percent(perc))
View(PercentGender)


#Correlation plot Matrix

CORR <- cor(Company[, unlist(lapply(Company, is.numeric))])
ggcorrplot(CORR,
           type = 'full',
           lab = TRUE,
           lab_size = 2.75,
           method = 'square',
           ggtheme= theme_bw ,
           colors = c('red', 'white', 'darkgreen'))

#Leave or not à l'air d'etre tres correlé avec le genre et l'annee d'arrivee, affichons graphe
ggplot(data = Company) +
  geom_bar(mapping = aes(x = Gender, fill = as.factor(LeaveOrNot)), position = 'dodge') +
  labs(x = "Gender", fill = "Leave or Not Leave")



Company_Num <- Company[, unlist(lapply(Company, is.numeric))]
Company_Num <- Company_Num[,-1] # Delete the first column
Company_Num$LeaveOrNot <- as.factor(Company_Num$LeaveOrNot)
head(Company_Num)

set.seed(2) #is used to fix the seed of the random draw

part.idx <- createDataPartition(Company_Num$LeaveOrNot, p=0.7, list = FALSE) 

train <- Company_Num[part.idx,] # creating the dataset "train" 
test <- Company_Num[-part.idx,] # creating the dataset "test"

dim(train)

round(table(train$LeaveOrNot)/nrow(train),2)

dim(test)

round(table(test$LeaveOrNot)/nrow(test),2)

#glm
glm.fit = glm(LeaveOrNot ~ .,data = train, family = 'binomial')
summary(glm.fit)

glm.pred = as.data.frame(predict(glm.fit, type = "response", newdata = test)) %>% 
  structure( names = c("pred_prob")) %>%
  mutate(pred = as.factor(ifelse(pred_prob > 0.5, "1", "0"))) %>% 
  mutate(actual = test$LeaveOrNot)
table(glm.pred$pred)

glm.conf = confusionMatrix(glm.pred$pred, glm.pred$actual, positive = "1")
glm.conf
table(test$LeaveOrNot,glm.pred$pred)

#rpart
rp.fit <- rpart(LeaveOrNot~., data=train)
summary(rp.fit)
prp(rp.fit)
rp.pred <- predict(rp.fit, test, type="class")
table(rp.pred)
rp.conf  <- confusionMatrix(rp.pred, test$LeaveOrNot)   
rp.conf
table(test$LeaveOrNot,rp.pred)


#Random Forest
rf.fit <- randomForest(LeaveOrNot~., data=train, ntree=500)
plot(rf.fit)
rf.pred   <- predict(rf.fit, test)
table(rf.pred)
rf.conf    <- confusionMatrix(rf.pred, test$LeaveOrNot)
rf.conf
table(test$LeaveOrNot,rf.pred)

#NaiveBayes
nb.fit <- naiveBayes(train, train$LeaveOrNot)
summary(nb.fit)
nb.pred <- predict(nb.fit, test)
table(nb.pred)
nb.conf <- confusionMatrix(nb.pred, test$LeaveOrNot)        
nb.conf
table(test$LeaveOrNot,nb.pred)

#compare model
couleur <- c("#FF0000", "#7FFF00")
par(mfrow=c(3,5))
fourfoldplot(rf.conf$table, color = couleur, conf.level = 0, margin = 1, main=paste("Random Forest (",round(rf.conf$overall[1]*100),"%)",sep=""))
fourfoldplot(nb.conf$table, color = couleur, conf.level = 0, margin = 1, main=paste("Naive Bayes (",round(nb.conf$overall[1]*100),"%)",sep=""))
fourfoldplot(rp.conf$table, color = couleur, conf.level = 0, margin = 1, main=paste("RPart (",round(rp.conf$overall[1]*100),"%)",sep=""))
fourfoldplot(glm.conf$table, color = couleur, conf.level = 0, margin = 1, main=paste("GLM (",round(glm.conf$overall[1]*100),"%)",sep=""))
