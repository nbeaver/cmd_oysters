JSON=$(wildcard *.json)
TIMESTAMP=$(patsubst %.json, timestamps/%.timestamp,$(JSON))

all: timestamps $(TIMESTAMP)

timestamps:
	mkdir timestamps

timestamps/%.timestamp : %.json
	../validate-oyster.py $< ../schemas/full-schema.json > $@

clean:
	rm -f $(TIMESTAMP)
