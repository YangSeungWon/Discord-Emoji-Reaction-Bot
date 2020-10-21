const Discord = require('discord.js');
const client = new Discord.Client();
const config = require("./config.json");
const db = require("./db.json");

const keys = Object.keys(db);

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
    for (let i=0, len = keys.length; i<len; i++) {
        let index = msg.content.indexOf(keys[i]);
        if (index == -1) continue;

        let timer = setTimeout(() => {
            msg.react(db[keys[i]]);
        }, index*500);
    }
});


client.login(config.token);

