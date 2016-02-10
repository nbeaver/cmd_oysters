JSON=$(wildcard *.json)
TIMESTAMP=$(patsubst %.json, timestamps/%.timestamp,$(JSON))

all: $(TIMESTAMP)

timestamps/%.timestamp : %.json
	../validate-oyster.py $< ../schemas/full-schema.json > $@ 

clean:
	rm -f $(TIMESTAMP)
