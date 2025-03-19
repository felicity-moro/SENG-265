#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// constant numbers 
#define DIRECT 1
#define REVERSE 2
#define MAX_L 4000
#define SECTIONS 5
#define MAX_Q 11
#define MAX_E 3000

// Question structure, used to hold string with question name, also stores frequency of each question
typedef struct{
    char ques[MAX_L];
    double fa;
    double a;
    double pa;
    double pd;
    double d;
    double fd;
} Question;

// Entry structure, stores all translated answers (in direct formating) in organized bidimensional array. Also stores averages of each section.
typedef struct{
    int responses_D[SECTIONS][MAX_Q];
    double c_avg;
    double i_avg;
    double g_avg;
    double u_avg;
    double p_avg;
    int is_null;

}Entry;

//reads stdin and returns the needed line via a pointer, asks how many lines to read from last reading
int read_line(char *line,int line_num){

    char holder[MAX_L];
    int counter = 0;

    FILE* filer = fopen("in02.txt","r");
    rewind(filer);

    while(fgets(holder,MAX_L,filer)){
        if (holder[0] != '#'){
            counter++;
            if (counter == line_num){
            strcpy(line,holder);
            printf("read line sucessful\n");
            return 1;
            }
        }
    }
    printf("END OF THE FILE\n");
    return -1;
    
}

//returns the testbits to main via pointer
void test_bits(int testbits[4]){
    char line[MAX_L];
    read_line(line,1);
    int j = 0;
    printf("testbits:\n");

    for (int i = 0; i < 4; i++){
        testbits[i] = (int)line[j] - 48;
        printf("%d ",testbits[i]);
        j = j+2;
    }
    printf("\n");
}

//stores all questions into question structs, and creates an organized bidimensional array that is returned via pointer
void get_guestion_names(Question worded[SECTIONS][MAX_Q]){
    char *tok;
    char line[MAX_L];
    read_line(line,2);
    
    tok = strtok(line,";\n");
    Question null_holder = {"###"};

    while(tok != NULL){
        //section c 8 questions
        for (int i = 0; i < 8; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[0][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[0][8] = null_holder;
        printf("names set C finished\n");

        //section I 10q
        for (int i = 0; i < 10; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[1][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[1][10] = null_holder; 
        printf("names set I finished\n");

        //section G 10q
        for (int i = 0; i < 10; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[2][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[2][10] = null_holder; 
        printf("names set G finished\n");

        //section U 6q
        for (int i = 0; i < 6; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[3][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[3][6] = null_holder; 
        printf("names set U finished\n");

        //section P 4q
        for (int i = 0; i < 4; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[4][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[4][4] = null_holder; 
        printf("names set P finished\n");
        printf("Get question names sucessful\n");

    } 
}

//returns 1 if question uses direct format, returns 2 if question uses reverse format
int direct(char *tok){
    int comparer = strcmp(tok,"Direct");
    int comparer1 = strcmp(tok,"Direct\n");
      if (comparer == 0 || comparer1 == 0){
            return DIRECT;
      }
      else {
            return REVERSE;
      }
}

//returns organized bidemsional int array where questions are direct or in reverse in same pattern as the question names, returned via pointer
void get_question_info(int questions[SECTIONS][MAX_Q]){

    char *tok;
    char line[MAX_L];
    read_line(line,3);
    tok = strtok(line,";\n");

    while(tok != NULL){
        //c first 8 questions
        for (int i = 0; i < 8; i++){
            int val = direct(tok);
            questions[0][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[0][8] = -1;
        printf("set C finished\n");

        //i 10q
        for (int i = 0; i < 10; i++){
            int val = direct(tok);
            questions[1][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[1][10] = -1;

        printf("set i finished\n");

        //g 10q
        for (int i = 0; i < 10; i++){
            int val = direct(tok);
            questions[2][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[2][10] = -1;
        printf("set g finished\n");

        //u 6q
        for (int i = 0; i < 6; i++){
            int val = direct(tok);
            questions[3][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[3][6] = -1;
        printf("set u finished\n");

        //p 4q
        for (int i = 0; i < 4; i++){
            int val = direct(tok);
            questions[4][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[4][4] = -1;
        printf("set p finished\n");
        printf("get question info sucessful\n");
    }
}

//returns value of likert answer in direct format. Will return -1 if token given is not a likert answer.
int likert_conversion(char answer[]){

    if (strcmp(answer,"fully disagree") == 0){
        return 1;
    }else if (strcmp(answer,"disagree") == 0){
        return 2;
    }else if (strcmp(answer,"partially disagree") == 0){
        return 3;
    }else if (strcmp(answer,"partially agree") == 0){
        return 4;
    }else if (strcmp(answer,"agree") == 0){
        return 5;
    }else if (strcmp(answer,"fully agree") == 0){
        return 6;
    }else{
        return -1; //not a likert answer
    }
}

//stores likert scale values in Question struct for ease. SKIPS ARRAY SPACE 0 SO LIKERT SCALE VAL IS SAME AS ARRAY VAL.
void store_likert(Question likert_scale[7]){

    char line[MAX_L];
    read_line(line,4);

    char *tok;
    tok = strtok(line,",\n");

    for (int counter = 1; counter < 7; counter++){
        Question holder;
        strcpy(holder.ques,tok);
        likert_scale[counter] = holder;
        tok = strtok(NULL,",\n");
    }

}

//reads an entry and returns it with, will return a null entry if no more entries to read
Entry read_entry(int* entry_counter){

    char line[MAX_L];
    int read = read_line(line, (*entry_counter) + 5);

    if (read == -1){
        Entry null;
        null.is_null = 1;
        return null;
    }

    Entry new_entry;
    char* tok = strtok(line,",\n");

    int counter = 0;
    int q = 0;

    //for section c 8q
    while (counter < 8){

        int likert_converted = likert_conversion(tok);

        if ( likert_converted != -1){
            new_entry.responses_D[0][q] = likert_converted;
            counter++;
            q++;
        }

        tok = strtok(NULL,",\n");
    }
    new_entry.responses_D[0][8] = -1;

    //for section I 10q
    counter = 0;
    q = 0;
    while (counter < 10){ 
        int likert_converted = likert_conversion(tok);

        if ( likert_converted != -1){
            new_entry.responses_D[1][q] = likert_converted;
            counter++;
            q++;
        }

        tok = strtok(NULL,",\n");
    }
    new_entry.responses_D[1][10] = -1;

    //for section G 10q
    counter = 0;
    q = 0;
    while (counter < 10){ 
        int likert_converted = likert_conversion(tok);

        if ( likert_converted != -1){
            new_entry.responses_D[2][q] = likert_converted;
            counter++;
            q++;
        }

        tok = strtok(NULL,",\n");
    }
    new_entry.responses_D[2][10] = -1;

    //for section u 6q
    counter = 0;
    q = 0;
    while (counter < 6){ 
        int likert_converted = likert_conversion(tok);

        if ( likert_converted != -1){
            new_entry.responses_D[3][q] = likert_converted;
            counter++;
            q++;
        }

        tok = strtok(NULL,",\n");
    }
    new_entry.responses_D[3][6] = -1;

    //for section p 4q
    counter = 0;
    q = 0;
    while (counter < 4){ 
        int likert_converted = likert_conversion(tok);

        if ( likert_converted != -1){
            new_entry.responses_D[4][q] = likert_converted;
            counter++;
            q++;
        }

        tok = strtok(NULL,",\n");
    }
    new_entry.responses_D[4][4] = -1;

    new_entry.is_null = 0;
    *entry_counter = *entry_counter + 1;
    printf("read entry sucessful\n");
    return new_entry;
}

//reads all entries and stores in given array
void store_and_read_entries(Entry entry_library[MAX_E], int* entry_counter){

    Entry holder = read_entry(entry_counter);
    entry_library[(*entry_counter) - 1] = holder;
    printf("entrycount for library %d\n", (*entry_counter) -1);


    while (holder.is_null != 1){
        printf("holder val is %d\n",holder.is_null);
        for(int i = 0; i < 5; i++){
        int j = 0;
            while (holder.responses_D[i][j] != -1){
            printf("%d ",entry_library[(*entry_counter) - 1].responses_D[i][j]);
            j++;
            }
            printf("entrycount %d\n", *entry_counter);
        }

        holder = read_entry(entry_counter);
        if (holder.is_null != 1){
            entry_library[(*entry_counter) - 1] = holder;
            printf("entrycount for library %d\n", (*entry_counter) -1);
        }
    } 

    printf("holder val is %d\n",holder.is_null);

}

//averages scores w/ correct direction for each section per respondent and puts in entry struct
void include_avgs(Entry question_library[MAX_E], int entry_counter, int question_direction[SECTIONS][MAX_Q]){
    if (entry_counter == 0){
        return;
    }

    for (int ent = 0; ent < entry_counter; ent++){

        printf("entry %d\n",ent+1);
        
        for (int sec = 0; sec < SECTIONS; sec++){
            int q = 0;
            double qvalue = 0;

            while(question_library[ent].responses_D[sec][q] != -1){

                if (question_direction[sec][q] == REVERSE){
                    qvalue += 7 - question_library[ent].responses_D[sec][q];

                }else if (question_direction[sec][q] == DIRECT){
                    qvalue += question_library[ent].responses_D[sec][q];
                }
                q++;
            }
            if (sec == 0){
                question_library[ent].c_avg = qvalue/8;
                printf("avg in sec c is %.2f\n",question_library[ent].c_avg);
            }
            if (sec == 1){
                question_library[ent].i_avg = qvalue/10;
                printf("avg in sec i is %.2f\n",question_library[ent].i_avg);
            }
            if (sec == 2){
                question_library[ent].g_avg = qvalue/10;
                printf("avg in sec g is %.2f\n",question_library[ent].g_avg);
            }
            if (sec == 3){
                question_library[ent].u_avg = qvalue/6;
                printf("avg in sec u is %.2f\n",question_library[ent].u_avg);
            }
            if (sec == 4){
                question_library[ent].p_avg = qvalue/4;
                printf("avg in sec p is %.2f\n",question_library[ent].p_avg);
            }

        }
        
    }
}

//stores frequencies of answers in question struct
void input_frequencies(Entry question_library[MAX_E],int entry_counter, Question questions[SECTIONS][MAX_Q]){

    for (int sec = 0; sec < SECTIONS; sec++){
        int q = 0;

        while(strcmp(questions[sec][q].ques,"###") != 0){
            
            questions[sec][q].fa = 0;
            questions[sec][q].a = 0;
            questions[sec][q].pa = 0;
            questions[sec][q].pd = 0;
            questions[sec][q].d = 0;
            questions[sec][q].fd = 0;

            for (int ent = 0; ent < entry_counter; ent++){
                if(question_library[ent].responses_D[sec][q] == 6){
                    questions[sec][q].fa+=1;
                }
                if(question_library[ent].responses_D[sec][q] == 5){
                    questions[sec][q].a+=1;
                }
                if(question_library[ent].responses_D[sec][q] == 4){
                    questions[sec][q].pa+=1;
                }
                if(question_library[ent].responses_D[sec][q] == 3){
                    questions[sec][q].pd+=1;
                }
                if(question_library[ent].responses_D[sec][q] == 2){
                    questions[sec][q].d+=1;
                }
                if(question_library[ent].responses_D[sec][q] == 1){
                    questions[sec][q].fd+=1;
                }
            }
            q++;
        }

    }

}

//averages section responces across all entries
void all_entry_avgs(double section_averages[SECTIONS], Entry question_library[MAX_E], int entry_counter){

    for (int sec = 0; sec < SECTIONS; sec++){
        double secavg = 0;

        for (int ent = 0; ent < entry_counter; ent++){

            if (sec == 0){
                secavg += question_library[ent].c_avg;
            }
            if (sec == 1){
                secavg += question_library[ent].i_avg;
            }
            if (sec == 2){
                secavg += question_library[ent].g_avg;
            }
            if (sec == 3){
                secavg += question_library[ent].u_avg;
            }
            if (sec == 4){
                secavg += question_library[ent].p_avg;
            }
        }

        section_averages[sec] = secavg/entry_counter;
        printf("section average of %d is %.2f\n",sec,section_averages[sec]);
    }

}

int main(){

    //stores the test bits into array of 4 for later excecution
    int testbits[4];
    test_bits(testbits);

    //question names stored in "questions" organized as [section][question]
    Question questions[SECTIONS][MAX_Q]; 
    get_guestion_names(questions);

    //question format directions stored in "questions_direction" organized as [section][question]
    int questions_direction[SECTIONS][MAX_Q];
    get_question_info(questions_direction);

    //stores likert scale strings(using Question struct) for printing to stdout
    Question likert_scale[7];
    store_likert(likert_scale);

    //holds all given entries, max of 3000 entries
    Entry entry_library[MAX_E];
    int entry_counter = 0; //gets incrememnted via pointer
    store_and_read_entries(entry_library,&entry_counter); 

    //inputs scores w/ proper direction value in Entry structure. Averages out the scores per section and stores in Entry structure
    include_avgs(entry_library,entry_counter,questions_direction);

    //stores answer frequency ammounts for each question in question struct
    input_frequencies(entry_library,entry_counter,questions);

    //saves the total section averages in total_avgs for later use
    double total_avgs[5];
    all_entry_avgs(total_avgs,entry_library,entry_counter);
    for (int i = 0; i < 5; i++){
        printf("sec avg %d is %.2f\n",i,total_avgs[i]);
    }
}




/*

for (int p = 0; p < 5; p++){

        for(int i = 0; i < 5; i++){
        int j = 0;
            while (entry_library[p].responses_D[i][j] != -1){
            printf("%d ",entry_library[p].responses_D[i][j]);
            j++;
            }
            printf("entrycount %d\n", entry_counter);
        }

    }

- read each line,

to read bidimensional array
for(int i = 0; i < 5; i++){
        int j = 0;
        while (questions[i][j] != 3){
            printf("%d ", questions[i][j]);
            j++;
        }
        printf("\n");
    }


   // i 10q
        for (int i = 0; i < 10; i++){
            Question holder = {*tok};
            worded[1][i] = holder;
            tok = strtok(NULL,";");
        }
        worded[1][10] = null_holder;
        printf("set I finished\n");

        // g 10q
        for (int i = 0; i < 10; i++){
            Question holder = {*tok};
            worded[2][i] = holder;
            tok = strtok(NULL,";");
        }
        worded[2][10] = null_holder;
        printf("set g finished\n");

        //u 6q
        for (int i = 0; i < 6; i++){
            Question holder = {*tok};
            worded[3][i] = holder;
            tok = strtok(NULL,";");
        }
        worded[3][6] = null_holder;
        printf("set U finished\n");

        //p 4q
        for (int i = 0; i < 4; i++){
            Question holder.ques = *tok;
            worded[4][i] = holder;
            printf("p question is: %s\n",worded[4][i].ques);
            tok = strtok(NULL,";");
        }
        worded[4][4] = null_holder;
        printf("set P finished\n");




    for(int i = 0; i < 5; i++){
        int j = 0;
        while (new_entry.responses[i][j] != -1){
            printf("%d ",new_entry.responses[i][j]);
            j++;
        }
        printf("entrycount %d\n",entry_counter);


        printf("testing question frequencies:\n");

    for(int sec = 0; sec < SECTIONS; sec++){
        int q = 0;
        printf("\n");

        while (strcmp(questions[sec][q].ques,"###") != 0){
            printf("%s\n",questions[sec][q].ques);
            printf("fa: %.2f\n",(questions[sec][q].fa/entry_counter)*100);
            printf("a: %.2f\n",(questions[sec][q].a/entry_counter)*100);
            printf("pa: %.2f\n",(questions[sec][q].pa/entry_counter)*100);
            printf("pd: %.2f\n",(questions[sec][q].pd/entry_counter)*100);
            printf("d: %.2f\n",(questions[sec][q].d/entry_counter)*100);
            printf("fd: %.2f\n",(questions[sec][q].fd/entry_counter)*100);
            q++;
        }
        printf("\n");

    }
    */
