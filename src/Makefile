# this rule require pdoc3. To install it, run "pip3 install pdoc3"
doc:
	bash -c "mkdir doc | rm -rf doc/*; cd game && pdoc --html --output-dir ../doc ../game"

tests:
	bash -c "./tests/run_tests.py -v"

.PHONY: doc tests runExample

runExample:
	bash -c "cd game; ./Game.py ai.playerTest.myPlayer ai.playerTest.myPlayer"

runAstar:
	bash -c "cd game; ./Game.py ai.playerTest.myPlayerAstar ai.playerTest.myPlayerAstar"
