# this rule require pdoc3. To install it, run "pip3 install pdoc3"
doc:
	bash -c "cd src; mkdir doc | rm -rf doc/*; cd game && pdoc --html --output-dir ../doc ../game"

tests:
	bash -c "./src/tests/run_tests.py -v"

.PHONY: doc tests runExample

runExample:
	bash -c "cd src/game; ./Game.py ai.playerTest.myPlayer ai.playerTest.myPlayer"

runAstar:
	bash -c "cd src/game; ./Game.py ai.playerTest.myPlayerAstar ai.playerTest.myPlayerAstar"

runBehavior:
	bash -c "cd src/game; ./Game.py ai.playerTest.myLittlePlayer ai.playerTest.myLittlePlayer"

runRotate:
	bash -c "cd src/game; ./Game.py ai.playerTest.rotatePlayer ai.playerTest.rotatePlayer"
