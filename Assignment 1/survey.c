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

    //increments ammount of lines forward, skips lines that are comments.
    while(fgets(holder,MAX_L,stdin)){
        if (holder[0] != '#'){
            counter++;
            if (counter == line_num){
            strcpy(line,holder);
            return 1;
            }
        }
    }
    return -1; // if there is no more to read
    
}

//returns the testbits to main via pointer
void test_bits(int testbits[4]){
    char line[MAX_L];
    read_line(line,1);
    int j = 0;

    //stores testbit numbers into the testbit array
    for (int i = 0; i < 4; i++){
        testbits[i] = (int)line[j] - 48;
        j = j+2;
    }
}

//stores all questions into question structs, and creates an organized bidimensional array that is returned via pointer
void get_guestion_names(Question worded[SECTIONS][MAX_Q]){
    char *tok;
    char line[MAX_L];
    read_line(line,1);
    
    tok = strtok(line,";\n");
    Question null_holder = {"###"}; //to signify where section stops

    while(tok != NULL){
        //for-loops below to store the names of questions into question structs in bidimensional organized by [section][question number] per section
        //section c 8 questions
        for (int i = 0; i < 8; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[0][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[0][8] = null_holder;

        //section I 10q
        for (int i = 0; i < 10; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[1][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[1][10] = null_holder; 

        //section G 10q
        for (int i = 0; i < 10; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[2][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[2][10] = null_holder; 

        //section U 6q
        for (int i = 0; i < 6; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[3][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[3][6] = null_holder; 

        //section P 4q
        for (int i = 0; i < 4; i++){   
            Question holder;
            strcpy(holder.ques,tok);
            worded[4][i] = holder;
            tok = strtok(NULL,";\n");
        }
        worded[4][4] = null_holder; 
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
    read_line(line,1);
    tok = strtok(line,";\n");

    while(tok != NULL){
        //for-loops below stores the direct/reverse value of each question in a array[sections][questions] per section
        //c first 8 questions
        for (int i = 0; i < 8; i++){
            int val = direct(tok);
            questions[0][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[0][8] = -1;

        //i 10q
        for (int i = 0; i < 10; i++){
            int val = direct(tok);
            questions[1][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[1][10] = -1;

        //g 10q
        for (int i = 0; i < 10; i++){
            int val = direct(tok);
            questions[2][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[2][10] = -1;

        //u 6q
        for (int i = 0; i < 6; i++){
            int val = direct(tok);
            questions[3][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[3][6] = -1;

        //p 4q
        for (int i = 0; i < 4; i++){
            int val = direct(tok);
            questions[4][i] = val; 
            tok = strtok(NULL,";\n");
        }
        questions[4][4] = -1;
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
    read_line(line,1);

    char *tok;
    tok = strtok(line,",\n");

    //stores likert strings in array of question structs for later printing
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
    int read = read_line(line,1);

    if (read == -1){ //if at end of file, return an entry with null value one to signify end of a entry library. main function to have a return value/for debugging
        Entry null;
        null.is_null = 1;
        return null;
    }

    Entry new_entry;
    char* tok = strtok(line,",\n");

    int counter = 0;
    int q = 0;

    //for-loops below store entry values in int array in entry struct. does this by section.
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
    return new_entry;
}

//reads all entries and stores in given array
void store_and_read_entries(Entry entry_library[MAX_E], int* entry_counter){

    Entry holder = read_entry(entry_counter);
    if (*entry_counter != 0){
        entry_library[(*entry_counter) - 1] = holder;
    }

    //reads remaining entries, stores in the given entry library array
    while (holder.is_null != 1){

        holder = read_entry(entry_counter);
        if (holder.is_null != 1){
            entry_library[(*entry_counter) - 1] = holder;
        }
    } 
}

//averages scores w/ correct direction for each section per respondent and puts in entry struct
void include_avgs(Entry question_library[MAX_E], int entry_counter, int question_direction[SECTIONS][MAX_Q]){
    if (entry_counter == 0){ //if no entries dont compute
        return;
    }

    //for every entry, for every section, for every question compare to see if the value should be direct or reverse
    //then change the likert value and add it to qvalue to average and store in entry struct
    for (int ent = 0; ent < entry_counter; ent++){
        
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
            }
            if (sec == 1){
                question_library[ent].i_avg = qvalue/10;
            }
            if (sec == 2){
                question_library[ent].g_avg = qvalue/10;
            }
            if (sec == 3){
                question_library[ent].u_avg = qvalue/6;
            }
            if (sec == 4){
                question_library[ent].p_avg = qvalue/4;
            }

        }
        
    }
}

//stores frequencies of answers in question struct
void input_frequencies(Entry question_library[MAX_E],int entry_counter, Question questions[SECTIONS][MAX_Q]){

    if (entry_counter == 0){ //if no entries dont compute
        return;
    }

    //for every section, for every question, cycle through all entries and save the frequencies of answers to the question struct
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
    if (entry_counter == 0){ //if no entries dont compute
        return;
    }

    //for all sections, cycle through all entries and average out all their answers and store into given array
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
    }

}

//prints title, always prints
void print_title(int entry_counter){
    
    printf("Examining Science and Engineering Students' Attitudes Towards Computer Science\n");
    printf("SURVEY RESPONSE STATISTICS\n\n");
    printf("NUMBER OF RESPONDENTS: %d\n\n",entry_counter);

}

//prints the start of output even if there are not entries
void print_item_one(int entry_counter, Question questions[SECTIONS][MAX_Q], Question likert_scale[7], int want_freqs){

    printf("FOR EACH QUESTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n\n");
    
    //for every section for every question print out the question and its frequencies using the stores likert scale
    for(int sec = 0; sec < SECTIONS; sec++){
        int q = 0;
        while (strcmp(questions[sec][q].ques,"###") != 0){
            printf("%s\n",questions[sec][q].ques);

            Question cur_entry = {"only use for holding averages",0,0,0,0,0,0};
            int entry_count = 1;

            if (entry_counter != 0 && want_freqs == 1){
                cur_entry = questions[sec][q];
                entry_count = entry_counter;
            }

            printf("%.2f: %s\n",(cur_entry.fd / entry_count) * 100, likert_scale[1].ques);
            printf("%.2f: %s\n",(cur_entry.d / entry_count) * 100, likert_scale[2].ques);
            printf("%.2f: %s\n",(cur_entry.pd / entry_count) * 100, likert_scale[3].ques);
            printf("%.2f: %s\n",(cur_entry.pa / entry_count) * 100, likert_scale[4].ques);
            printf("%.2f: %s\n",(cur_entry.a / entry_count) * 100, likert_scale[5].ques);
            printf("%.2f: %s\n\n",(cur_entry.fa / entry_count) * 100, likert_scale[6].ques);

            q++;
        }
    }

}

//prints the second item 
void print_item_two(int entry_counter, Entry entry_library[MAX_E]){
    printf("SCORES FOR ALL THE RESPONDENTS\n\n");

    //for every entry print out the average of each section of that entry into a line
    for (int ent = 0; ent < entry_counter; ent++){
        printf("C:%.2f,I:%.2f,G:%.2f,U:%.2f,P:%.2f\n",entry_library[ent].c_avg, entry_library[ent].i_avg, entry_library[ent].g_avg, entry_library[ent].u_avg, entry_library[ent].p_avg);
    }
}

//prints the third item
void print_item_three(double total_avgs[SECTIONS]){

    printf("AVERAGE SCORES PER RESPONDENT\n\n");
    printf("C:%.2f,I:%.2f,G:%.2f,U:%.2f,P:%.2f\n",total_avgs[0], total_avgs[1], total_avgs[2], total_avgs[3], total_avgs[4]);

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
    double total_avgs[SECTIONS] = {0,0,0,0,0};
    all_entry_avgs(total_avgs,entry_library,entry_counter);


    //FUNCTIONS USED TO PRINT OUTPUT DEPENDING ON TESTBITS

    print_title(entry_counter);

    if (testbits[0] == 1){
        print_item_one(entry_counter,questions,likert_scale,0);
    }
    if (testbits[1] == 1){
        print_item_one(entry_counter,questions,likert_scale,1);
    }
    if (testbits[2] == 1){
        print_item_two(entry_counter,entry_library);
    }
    if (testbits[3] == 1){
        print_item_three(total_avgs);
    }
    
    //code finished
    return 0;
}