#!/bin/bash


FILES_DIR="./macros"
FILES="$FILES_DIR/*.py"
OUTPUT_DIR="./release"
# Create directory if does not exists.
[ -d $OUTPUT_DIR ] || mkdir $OUTPUT_DIR

for FILE in $FILES
do

    FILENAME=$(basename -- "$FILE")
    EXTENSION="${FILENAME#*.}"

    # Double check the extension is a python file
    if [ "$EXTENSION" = "py" ]; then 
        NEW_FILE="$OUTPUT_DIR/${FILENAME%%.*}.FCMacro"
    else
        NEW_FILE="$OUTPUT_DIR/$FILENAME"
    fi

    if [ -e $NEW_FILE ]; then
        CHANGE=diff $FILE $NEW_FILE

        if [ $CHANGE -eq 0 ]; then
            echo "No changes on $FILE"
        else
            echo "Converting file $FILENAME to $NEW_FILE"
            # Make a temporary convertion.
            cp $FILE $NEW_FILE
        fi
    else
        echo "Converting file $FILENAME to $NEW_FILE"
        # Make the final convertion.
        cp $FILE $NEW_FILE
    fi

    


    
    
done