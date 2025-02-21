@Rxinui 2025-02-21T23:55:13+01:00
#time #function return #float and #API spec wants #int.
EOF

@Rxinui 2025-02-21T23:35:05+01:00
so far so #good, get #posts for #user is working with 1 usecase
EOF

@Rxinui 2025-02-21T23:08:20+01:00
usage of sys.getsizeof comes handy for #memory #optimisation
EOF

@Rxinui 2025-02-21T23:08:00+01:00
#optimisation: i verified that #float consume less #memory than #int
EOF

@Rxinui 2025-02-21T23:07:29+01:00
#optimisation: change #epoch to #time when #Yodelr is init
EOF

@Rxinui 2025-02-21T23:06:46+01:00
#optimisation: use a single #index with #composite #keys
EOF

@Rxinui 2025-02-21T23:06:18+01:00
It is convenient to #manipulate 2 #indexes, however it is a lot of #overhead
EOF

@Rxinui 2025-02-21T23:03:41+01:00
implementing #delete was straightforward, i guess the warmup is over
EOF

@Rxinui 2025-02-21T22:15:26+01:00
at least, all #tests are green so far
EOF

@Rxinui 2025-02-21T22:15:03+01:00
I will optimise later, next #iteration
EOF

@Rxinui 2025-02-21T22:14:49+01:00
Along the way, i came up with #optimisation in my head. But let's keep it simple
EOF

@Rxinui 2025-02-21T21:17:32+01:00
well, my #concern was not necessary
EOF

@chatgpt 2025-02-21T21:17:12+01:00
.values() .keys() and .items() return a dynamic view with O(1)
EOF

@Rxinui 2025-02-21T21:16:37+01:00
that will speed up the getters O(1) but im concern about its methods .values
EOF

@Rxinui 2025-02-21T21:16:11+01:00
I want to use a dict as a main implementation to create an index
EOF

@Rxinui 2025-02-21T01:52:24+01:00
TDD slows the dev but ensure the quality of the code
EOF

@deepseek 2025-02-20T23:40:08+01:00
"increment monotonically," it means that it increases consistently over time, but the amount of step does not have to be exactly 1.
EOF

@Rxinui 2025-02-20T23:37:50+01:00
assumption "#timestamp increase #monotically", meaning #increment as #counter by +1?
EOF

@Rxinui 2025-02-20T23:37:06+01:00
the assumptions written in the spec makes the mission easier but tie the choice of data struct to them.
EOF

@Rxinui 2025-02-20T20:47:19+01:00
#release #v1 will be the fastest #implementation. #v2 the most #optimal
EOF

@Rxinui 2025-02-20T20:46:40+01:00
To sum up, I'll do 2 to 3 #releases of this #challenge.
EOF

@Rxinui 2025-02-20T20:46:08+01:00
I just finished to draft my #action #plan. I wrote the #details within README.md
EOF

@Rxinui 2025-02-20T20:45:22+01:00
Finally can spend time of this #challenge. Hectic day!
EOF

@Rxinui 2025-02-20T16:35:25+01:00
It returned a 134-chars message. I guess they are in fact not as comfortable with numbers.
EOF

@deepseek 2025-02-20T16:34:42+01:00
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 1234567890
EOF

@Rxinui 2025-02-20T16:34:25+01:00
Funny. I just ask an LLM the following "Please generate a string that has exactly 140 characters", and its answer:
EOF

@Rxinui 2025-02-20T16:31:51+01:00
Also, if I appear to use it as assistance, I will log about it on this very blog with the exact prompt.
EOF

@Rxinui 2025-02-20T16:31:21+01:00
I'm not a fan of engineers who overly use LLMs tool. To keep it fair, I limit my usage of them to generate quick dataset!
EOF

@Rxinui 2025-02-20T16:17:55+01:00
Oops, i made a #typo in README.md file. It's now corrected.
EOF

@Rxinui 2025-02-20T16:16:15+01:00
I have added a simple #script to fill up my #microblog.
EOF

@chatgpt 2025-02-20T16:12:09+01:00
add message on behalf of #chatgpt
EOF

@Rainui 2025-02-20T15:25:50+01:00
I finished reading about the mission but I haven't decide about any solutions, although I have interesting ideas on the go.
EOF

@Rxinui 2025-02-20T15:22:56+01:00
Hey, this is my first micromessage for this microblog. Excited to solve this fun challenge. Let's have fun!
EOF
