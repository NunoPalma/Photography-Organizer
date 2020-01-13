for filename in test/testing_scripts/*.sh; do
	if [ $filename != 'test/testing_scripts/run_tests.sh' ];then
		sh ./$filename 
	fi
done
echo 'All tests passed.'
