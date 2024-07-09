library(jsonlite)
library(tidyverse)
library(kableExtra)

## PArte 1 results compilation

path <- "~/Evaluación gpt-latino/CHILE - PSU/repo/ProyectoDL/results/"

tests_list<-list.files(path)

tests_list <- tests_list[-1]

test<- tests_list[1]





df <- fromJSON(paste0(path,test))%>%
  as.data.frame()




df<-df%>%
  rename(answer=1)%>%
  select(1)%>%
  mutate(test=str_remove_all(test,".json"))%>%
  separate(test,into = c("st","Model","Country","subject","trial_id"),sep="_")%>%
  mutate(subject=case_when(is.na(subject)~"Revisar!",
                        .default = subject))



df<-df%>%
  mutate(item_id=NA)%>%
  filter(is.na(st))%>%
  relocate(item_id=1)
  



for(i in tests_list){
  
  
  
  data <- fromJSON(paste0(path,i))%>%
    as.data.frame()%>%
    rename(answer=1)%>%
    select(1)%>%
    mutate(test=str_remove_all(i,".json"))%>%
    separate(test,into = c("st","Model","Country","subject","trial_id"),sep="_")%>%
    mutate(trial_id=as.numeric(trial_id))
    
  
  data<-data%>%
    mutate(item_id=c(1:length(data[,1])))
  
    
  
    df<-df%>%
      rbind(data)
}


 


## Questionaires compilation


path <- "~/Evaluación gpt-latino/CHILE - PSU/repo/ProyectoDL/data/pruebas_mmlu/"

tests_list<-list.files(path)


tests_list<- tests_list[1:4]

rel<-data.frame(test=tests_list,
                Country=c(
                "chile",
                "chile",
                "colombia",
                "colombia"),
                subject=c(
                "historia",
                "lenguaje",
                "historia",
                "lenguaje"))


test_df <- fromJSON(paste0(path,tests_list[2]))%>%
  as.data.frame()




test_df<-test_df%>%
  rename(key=3)%>%
  select(1,3)%>%
  mutate(test=tests_list[2])%>%
  left_join(rel,by="test")




test_df<-test_df%>%
  mutate(item_id=NA)%>%
  filter(is.na(1))%>%
  relocate(item_id=1)




for(i in tests_list){
  
  
  
  data <- fromJSON(paste0(path,i))%>%
    as.data.frame()%>%
    rename(key=3)%>%
    select(1,3)%>%
    mutate(test=i)%>%
    left_join(rel,by="test")
  
  
  data<-data%>%
    mutate(item_id=c(1:length(data[,1])))
  
  
  
  test_df<-test_df%>%
    rbind(data)
}



df<-df%>%
  left_join(test_df[,c(2,4,5,6)],
            by=c("Country","subject","item_id"),
            relationship = "many-to-many")%>%
  mutate(correct=case_when(answer==key~1,
                           answer!=key~0))



save(df,test_df,file="eval_results.Rdata")
