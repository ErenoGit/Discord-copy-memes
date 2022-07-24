const { Client, GatewayIntentBits, Partials } = require('discord.js');
var mysql = require('mysql');

require('dotenv').config();
const Discord = require("discord.js");
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildWebhooks], 
    partials: [Partials.Channel, Partials.Message] });

    
client.on("ready", () => {
  console.log(`Logged in as ${client.user.tag}!`)
})

const sendNewMemes = () => {  
  try {
    console.log(`sendNewMemes started`)

    var tableOfNewMemes = []
    var tableOfAlreadyExistingMemes = []

    var con = mysql.createConnection({
      host: "host",
      user: "user",
      password: "password",
      database: "database"
    });
    con.connect();
    con.query("SELECT link FROM memes ORDER BY ID DESC LIMIT 50;", function (err, result, fields) {
      if (err) throw err;
      result.forEach(function(row) {
        tableOfNewMemes.push(row.link);
      })
    });

    var channel = client.channels.cache.get(process.env.TARGET_CHANNEL_ID);
    channel.messages.fetch({ limit: 100 }).then(messages => {
      messages.forEach(message => tableOfAlreadyExistingMemes.push(message.content))
    })

    setTimeout(function() {
      tableOfNewMemes.forEach(function(element) {
        if(!tableOfAlreadyExistingMemes.includes(element)){
          channel.send(element);  
        }
      })
    console.log(`sendNewMemes ended`)
    }, 5000);
  }
  catch (err){
    console.log(err);
  }
  finally {
    setTimeout(function() {
      console.log(`connection closed`)
      con.end();
  }, 5000);
  }
};  

setInterval(sendNewMemes, 600000); // run the sendMessage() function every 10 minutes (600000 miliseconds)


client.login(process.env.DISCORD_TOKEN);
