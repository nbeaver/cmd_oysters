JSON=$(wildcard *.json)
TIMESTAMP=$(patsubst %.json, timestamps/%.timestamp,$(JSON))

all: timestamps $(TIMESTAMP)

timestamps:
	mkdir timestamps

timestamps/%.timestamp : %.json
	../validate_oyster.py $< ../schemas/full-schema.json
	touch $@ # update the timestamp only if validation succeeds

clean:
	rm -f $(TIMESTAMP)
