const Discord = require('discord.js');
const client = new Discord.Client();
const config = require("./config.json");
const db = require("./db.json");

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
    let content = msg.content;

    let keys = Object.keys(db);
    let changed = false;
    for (let i=0, len = keys.length; i<len; i++) {
        while (content.includes(keys[i])){
            changed = true;
            content = content.replace(keys[i], db[keys[i]]);
        }
    }
    
    if (changed){
        msg.delete({ timeout: 0 }).catch(console.error);
        const _embed = new Discord.MessageEmbed()
            .setAuthor(msg.author.username,msg.author.displayAvatarURL())
            .setDescription(content);
        msg.channel.send(_embed);
    }
});


client.login(config.token);

