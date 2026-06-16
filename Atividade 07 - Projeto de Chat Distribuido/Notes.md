# Projeto de Sistemas Distribuidos - Atividade 07

Discente: Norman Vinícius Pereira dos Santos

---

## QUESTIONÁRIO (Google Classroom):

Complemento da Atividade 06.

*Mesma DUPLA. da Atividade 06*

*Com a atividade 6 pronta, implemente os seguintes requisitos.*

Quando o cliente se conectar, ele terá que informar o seu nome (nickname). (Error, Usuário já conectado)

O Chat agora em vez de enviar para todos, ira enviar para uma pessoa ou grupo de pessoas especifico de acordo com o comando solicitado.

### Comandos Novos

Conectado o Cliente pode mandar comandos para o servidor  

- listarusuarios (recebe a lista de todos os usuários) 
- criargrupo (cria um grupo),
- criargrupo NOME_DO_GRUPO , (Error, grupo já existente)
- listargrupos (recebe a lista de todos os grupos) 
- listargrupos (Erro, nenhum grupo cadastrado)
- listausrgrupo (listar todos os usuários do grupo especifico ) 
- listausrgrupo NOME_DO_GRUPO  (Erro, grupo cadastrado não cadastrado)
- entrargrupo (entrar no grupo de nome X), 
- entrargrupo NOME_GRUPO (Erro grupo não existe)
 sairgrupo (entrar no grupo de nome X),  -sairgrupo NOME_GRUPO (Erro grupo não existe)
- msg ( "U" usuário, "G" grupo) ; 
- msg U ou G NICK/GRUPO MENSAGEM
- msgt ("C" mensagem para todos os usuário online;    "D" mensagem para todos os usuário desconectados; "T" todos os usuários)  -msgt C ou D ou T MESAGEM

Para qualquer outro comanda exibir a mensagem comando inexistente,   

Para um usuário mandar uma mensagem tem que usar o comando -msg ou -msgt. Caso o usuário não esteja online no momento, ele deverá receber a mensagem quando ficar online, logo o servidor tem que armazenar a mensagem recebida e enviar ao usuário quando ele ficar online.   

Caso a mensagem seja enviada para o grupo os pertencentes ao grupo terão que receber a mensagem que o grupo recebeu. 

Toda Mensagem que chega no servidor terá que ser alterada da seguinte forma: na frente da mensagem entre PARENTESE () será adicionado o NICK do usuário que enviou a msg, e caso seja uma mensagem enviada para um grupo o nome do grupo também terá que ser adicionado após o NICK separado por virgula, e após os dois a HORA/DATA da mensagem. (NICK, GRUPO, DATA/HORA) MENSAGEM

*Caso o comando seja  invalido ou com parâmetros errado informar o ERRO*

### O que tem ser entregue:
Código Sem COMPACTAR. Se vim compactado não corrijo.
Pequeno vídeo mostrando o funcionamento.

---

## Norman's Notes

Eu costumo escrever, pensar e programar em Inglês.

For this one, I know I was supposed to, say, update the previous code, but I felt like I couldn't work with it. Not only that, but I felt like it needed a GUI, even a simple one. So I wroked on the project from scratch.

### TODO

[ ] Add commands
[ ] Add "Error, Usuário já conectado" if entering a user with an existing name.

[ ] Add command "/listarusuarios" that returns a list with every user 
[ ] Add command "/criargrupo [nome]" that creates a group with a given name and adds the creator to the group,
[ ] Add command "/criargrupo [nome]" that displays an error if the group is already created
[ ] Add command "/listargrupos" that shows a list of all the groups
[ ] Add command "/listargrupos" throws an erro if there is no group
[ ] Add command "/listausrgrupo [gropo_nome]" returns a list of every user of a group
[ ] Add command "/listausrgrupo [grupo nome]" throws an erro if said groupd doesn't exist
[ ] Add command "/entrargrupo [grupo_nome]" adds the user to said group, 
[ ] Add command "/entrargrupo [grupo_nome]" throws an erro if said group does't exit
[ ] Add command "/sairgrupo [grupo_nome]" removed said user from the group,  
[ ] Add command "/sairgrupo [grupo_nome]" throws an erro if group doesn't exist
[ ] Add command "/msg USERNAME [MENSAGEM]" sends a message only to the user USERNAME; 
[ ] Add command "/msg GROUP [MENSAGEM]" sends a message only to the group GROUP; 
[ ] Add command "/msgt [LETTER] [MENSAGEM]" and the letter can be "C" (mensagem para todos os usuário online), "D" (mensagem para todos os usuário desconectados), "T" (todos os usuários)





color 2 & cd OneDrive\Documents\College Subjects\2026.1 Projeto de Sistemas Distribuidos (PSD)\Atividade 07 - Projeto de Chat Distribuido\src & python "server.py"
color 3 & cd OneDrive\Documents\College Subjects\2026.1 Projeto de Sistemas Distribuidos (PSD)\Atividade 07 - Projeto de Chat Distribuido\src & python "client.py"
