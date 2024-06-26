validate_token_response = {
    "active": True,
    "client_id": "oauth2_tide",
    "token_type": "Bearer",
    "username": "test_user",
    "scope": "profile user_tasks user_courses",
    "aud": "oauth2_tide",
    "exp": 864000,
    "iat": 1713772959,
}

get_profile_test_response = {
    "id": 11111111,
    "emails": [{"email": "test@test.fi", "verified": True}],
    "last_name": "Test",
    "given_name": "Test",
    "real_name": "Test Test",
    "username": "test_user",
}

get_ide_courses_test_response = [
    {
        "name": "Testikurssi",
        "id": 111111,
        "path": "kurssit/testi/test/",
        "tasks": [
            {
                "name": "Demo1",
                "path": "kurssit/testi/test/demot/Demo1",
                "doc_id": 1111111,
            },
            {
                "name": "Demo2",
                "path": "kurssit/testi/test/demot/Demo2",
                "doc_id": 2222222,
            },
        ],
    }
]

get_tasks_by_doc_test_response = [
    {
        "task_files": [
            {
                "task_id_ext": "111.test.test",
                "content": '#include <stdio.h>\n\nvoid ohjeet(void)\n{\n  printf("Ohjelma laskee huoneen '
                'pinta-alan ja tilavuuden annettujen tietojen perusteella.");\n\n}\n\n/* Kirjoita '
                "tarvittavat aliohjelmat */\n\nint main(void)\n{\n  ohjeet();\n\n  /* Täydennä "
                "ohjelman toiminta */\n\n  return 0;\n}",
                "file_name": "test.c",
                "user_input": "3 4 2.5",
                "user_args": "",
            }
        ],
        "path": "kurssit/testi/test/demot/Demo1",
        "header": None,
        "stem": None,
        "type": "cc/input/comtest",
        "task_id": "testi",
        "doc_id": 1,
        "par_id": "asd",
        "ide_task_id": "t1",
    },
    {
        "task_files": [
            {
                "task_id_ext": "222.test.test",
                "content": '#include <stdio.h>\n\nvoid ohjeet(void)\n{\n  printf("Ohjelma laskee huoneen '
                'pinta-alan ja tilavuuden annettujen tietojen perusteella.");\n\n}\n\n/* Kirjoita '
                "tarvittavat aliohjelmat */\n\nint main(void)\n{\n  ohjeet();\n\n  /* Täydennä "
                "ohjelman toiminta */\n\n  return 0;\n}",
                "file_name": "test.c",
                "user_input": "3 4 2.5",
                "user_args": "",
            }
        ],
        "path": "kurssit/testi/test/demot/Demo1",
        "header": None,
        "stem": None,
        "type": "cc/input/comtest",
        "task_id": "testi",
        "doc_id": 2,
        "par_id": "asd",
        "ide_task_id": "t2",
    },
]

get_task_by_ide_task_id_test_response = {
    "task_files": [
        {
            "task_id_ext": "333.test.test",
            "content": '#include <stdio.h>\n\nvoid ohjeet(void)\n{\n  printf("Ohjelma laskee huoneen '
            'pinta-alan ja tilavuuden annettujen tietojen perusteella.");\n\n}\n\n/* Kirjoita '
            "tarvittavat aliohjelmat */\n\nint main(void)\n{\n  ohjeet();\n\n  /* Täydennä "
            "ohjelman toiminta */\n\n  return 0;\n}",
            "file_name": "test.c",
            "user_input": "3 4 2.5",
            "user_args": "",
        }
    ],
    "path": "kurssit/testi/test/demot/Demo1",
    "header": None,
    "stem": None,
    "type": "cc/input/comtest",
    "task_id": "test",
    "doc_id": 3,
    "par_id": "asd",
    "ide_task_id": "t3",
}

submit_task_by_id_test_submit = {
    "code_files": [
        {
            "task_id_ext": "1111.test.asd",
            "content": '#include <stdio.h>\n\nint main(void)\n{\n  printf("Hello, World!\\n");\n\n  return '
            "0;\n}",
            "file_name": "test.c",
            "source": "editor",
            "user_input": "",
            "user_args": "",
        }
    ],
    "code_language": "cc",
}

submit_task_by_id_tim_test_response = {
    "result": {
        "web": {
            "console": "Hello, World!\n",
            "error": "",
            "pwd": "",
            "language": None,
            "runtime": "0.883   0.872\nCompile time:\nreal\t0m0.105s\nuser\t0m0.039s\nsys\t0m0.022s\n\nRun "
            "time:\nreal\t0m0.001s\nuser\t0m0.001s\nsys\t0m0.000s\n",
        },
        "savedNew": 111111,
        "valid": True,
    },
    "plugin": None,
}
