# Pierpaolo - a lyrical text system

Pierpaolo is a lyrical text system.

## Program structure 

A Pierpaolo program is a sequence of statements or *verses*. 

All Pierpaolo programs must begin with the line

    PIERPAOLO <TITLE>
    
where `<TITLE>` stands for the title of your Pierpaolo program; and end either with

    BRAVO
    
in which case the program terminates or

    BRAVISIMO
    
in which case the program must terminate *and* save its log to the file `<TITLE>.CSV`. Note that Pierpaolo verses must be in UPPERCASE so the audience will be able to hear. Programs with lowercase characters will compile but rob your characters of some pleasure. 

Comments start with one of the keywords

    NOTE THAT

    REALIZE THAT

    LAMENT THAT

## Characters

Characters can be introduced to a Pierpaolo program with the verse

    INTRODUCE <NAME>
    
where `<NAME>` can be any name suitable to your program EXCEPT `MARCELLA` and `GESUALDO`. Pierpaolo programs containing these names will crash your computer. Otherwise, characters cannot be killed once introduced.

## Time and movement

A Pierpaolo program is characterized by the movement of characters as time progresses. Characters therefore have a (t, x) location where t is the current time and x is the horizontal location; equivalently, the time coordinate can be explained to the audience as a vertical location such that time sweeps the characters forward inexorably.

Time must be advanced in discrete units by entering a verse saying exactly

    SO
    
If not otherwise scheduled, characters will move to the left with probability 1/2 and to the right with probability 1/2. The simplest form of scheduling is the verse

    MOVE <NAME> LEFT
    
 (or accordingly `RIGHT`). This schedule will last one time interval; therefore the program
 
     PIERPAOLO README
     
     INTRODUCE MARIA
     MOVE MARIA LEFT
     SO
     
     INTRODUCE MATEO
     NOTE THAT MARIA IS UNSCHEDULED
     MOVE MATEO RIGHT
     SO
     
     BRAVO
     
works as follows: in the first step `MARIA` is introduced and scheduled to move from (0,0) to (1,-1). Then in the next pulse `MATEO` is introduced and scheduled to move to (1,1); meanwhile `MARIA` is unscheduled and could go either to (2,-2) or (2,0).

## Monuments and pleasure

A monument is a fixed thing set by the verse

    SET <MONUMENT NAME> AT (x,y)
    
where (x,y) are floats and monument names are uncensored. 

Monuments allow a new form of scheduling characters as the following verse shows:

    SEND <NAME> TOWARD <MONUMENT NAME>
    
 This will cause characters to move in straight line until their Euclidean distance to the monument is less or equal than 1 (this event is referred as *crashing*). After a crash, characters become unscheduled again and begin moving randomly. 
 
 Monuments are initially neutral, but they can cause pleasure or displeasure with any of the following verses
 
     MAKE <MONUMENT NAME> PLEASURABLE
 
     MAKE 
 
 Likewise the following verse
 
    MAKE <NAME1> CHASE <NAME2>
 
 causes the character `NAME1` move towards the straight line toward where `NAME2` currently is. Chases also stop with a crash, although they're likely to last indefinitely.
 
 
