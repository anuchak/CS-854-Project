# Steps for setting up vLLM

(1) cmd to run: 
nohup vllm serve Qwen/Qwen3-32B     --dtype=auto     --trust-remote-code     --port=8000     --tensor-parallel-size 4 --enforce-eager     > vllm_server.log 2>&1 &

(2) $LD_LIBRARY_PATH
/home/abtinmy/projects/aip-xihe/abtinmy/CS-854-Project/level-zero-1.26.0/build/lib:/home/abtinmy/projects/aip-xihe/abtinmy/CS-854-Project/linux-6.8/tools/power/cpupower:/home/abtinmy/projects/aip-xihe/abtinmy/CS-854-Project/libjpeg-turbo:/home/abtinmy/projects/aip-xihe/abtinmy/CS-854-Project/openjpeg/build:/home/abtinmy/projects/aip-xihe/abtinmy/CS-854-Project/openjpeg/build/bin:/home/abtinmy/libs/libedit/lib





