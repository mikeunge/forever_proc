# forever_proc

#### ⚡ Monitor forever.js processes

​	

`this.tool` is here to help you monitor and **automate your server processes**.



If you're like me and run many bots/scripts as daemons, you probably came across the **forever.js tool**.



This tool is ✨ **AMAZING** ✨ and I use it basically for everything that needs to be run without my consent.



After some weird crashes, I noticed a weakness in the way I run my bots.. they don't automatically start themselves after crashing 😨.



This is why I wrote this little script. It checks if a bot/script is running, if not it tries to spin up a new instance. 



Feel free to use it and contribute if you have good ideas on how to make it better, thanks and bye 👋



## Todo 📖

- [ ] Check if forever process is actually running and not on "**STOPPED**"

- [ ] Add folder and file checks before running the commands; handing them to the "***jobController***"

- [x] Add a Changelog.md

- [ ] Smart Mailing (*if a script is not able to start, send an email to admin*)