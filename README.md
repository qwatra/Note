MyNotes
=======

Web-приложение для хранения заметок. Заметки можно добавлять, удалять, редактировать, сортировать, фильтровать и публиковать.
+ Для добавления заметки нажмите кнопку "Добавить заметку".
+ Для редактирования заметки кликните по "стикеру" с заметкой
+ Для удаления заметки кликните по крестику в верхнем правом углу стикера.
+ Для того, чтобы сделать заметку избранной кликните по галочке в верхнем левом углу стикера (галочка появляется при наведении курсора на аметку)
+ Для публикации замекти войдите в режим редактирования(кликните по "стикеру" с заметкой) и в открывшимся окне заполните поле "идентификатор" и установите флажок в поле "Публичная заметка". После этого любой желающий сможет получить доступ к вашей заметке по ссылке:   
    ```/note/<имя пользователя>/<идентификатор заметки>```
+ Для сортировки и фильтрации заметок воспользуйтесь соотвесвующими формами.

Зависимости
-----------
+ Django==2.1.1
+ django-bootstrap4==0.0.7
+ django-tinymce==2.7.0
