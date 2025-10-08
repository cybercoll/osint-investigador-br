# -*- coding: utf-8 -*-
import sqlite3
import os
from datetime import datetime
import hashlib

class DatabaseManager:
    def __init__(self, db_path="osint_database.db"):
        """Inicializa o gerenciador de banco de dados"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Cria as tabelas necessárias se não existirem"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela principal para dados pessoais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT UNIQUE NOT NULL,
                nome TEXT,
                rg TEXT,
                cnh TEXT,
                email TEXT,
                telefone TEXT,
                titulo_eleitor TEXT,
                pis TEXT,
                cns TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para otimizar buscas
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cpf ON pessoas(cpf)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_nome ON pessoas(nome)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rg ON pessoas(rg)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cnh ON pessoas(cnh)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON pessoas(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_telefone ON pessoas(telefone)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_titulo_eleitor ON pessoas(titulo_eleitor)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pis ON pessoas(pis)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cns ON pessoas(cns)')
        
        conn.commit()
        conn.close()
    
    def inserir_pessoa(self, cpf, nome=None, rg=None, cnh=None, email=None, telefone=None, titulo_eleitor=None, pis=None, cns=None):
        """Insere uma nova pessoa no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO pessoas (cpf, nome, rg, cnh, email, telefone, titulo_eleitor, pis, cns)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cpf, nome, rg, cnh, email, telefone, titulo_eleitor, pis, cns))
            
            conn.commit()
            return {"status": "success", "message": "Pessoa inserida com sucesso"}
        
        except sqlite3.IntegrityError:
            return {"status": "error", "message": "CPF já existe no banco de dados"}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao inserir pessoa: {str(e)}"}
        finally:
            conn.close()
    
    def atualizar_pessoa(self, cpf, nome=None, rg=None, cnh=None, email=None, telefone=None, titulo_eleitor=None, pis=None, cns=None):
        """Atualiza dados de uma pessoa existente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Construir query dinamicamente baseado nos campos fornecidos
            campos_update = []
            valores = []
            
            if nome is not None:
                campos_update.append("nome = ?")
                valores.append(nome)
            if rg is not None:
                campos_update.append("rg = ?")
                valores.append(rg)
            if cnh is not None:
                campos_update.append("cnh = ?")
                valores.append(cnh)
            if email is not None:
                campos_update.append("email = ?")
                valores.append(email)
            if telefone is not None:
                campos_update.append("telefone = ?")
                valores.append(telefone)
            if titulo_eleitor is not None:
                campos_update.append("titulo_eleitor = ?")
                valores.append(titulo_eleitor)
            if pis is not None:
                campos_update.append("pis = ?")
                valores.append(pis)
            if cns is not None:
                campos_update.append("cns = ?")
                valores.append(cns)
            
            if not campos_update:
                return {"status": "error", "message": "Nenhum campo para atualizar"}
            
            campos_update.append("data_atualizacao = CURRENT_TIMESTAMP")
            valores.append(cpf)
            
            query = f"UPDATE pessoas SET {', '.join(campos_update)} WHERE cpf = ?"
            cursor.execute(query, valores)
            
            if cursor.rowcount > 0:
                conn.commit()
                return {"status": "success", "message": "Pessoa atualizada com sucesso"}
            else:
                return {"status": "error", "message": "CPF não encontrado"}
        
        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar pessoa: {str(e)}"}
        finally:
            conn.close()
    
    def buscar_por_cpf(self, cpf):
        """Busca uma pessoa pelo CPF"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM pessoas WHERE cpf = ?', (cpf,))
            resultado = cursor.fetchone()
            
            if resultado:
                return {
                    "status": "success",
                    "dados": {
                        "id": resultado[0],
                        "cpf": resultado[1],
                        "nome": resultado[2],
                        "rg": resultado[3],
                        "cnh": resultado[4],
                        "email": resultado[5],
                        "telefone": resultado[6],
                        "titulo_eleitor": resultado[7],
                        "pis": resultado[8],
                        "cns": resultado[9],
                        "data_criacao": resultado[10],
                        "data_atualizacao": resultado[11]
                    }
                }
            else:
                return {"status": "not_found", "message": "CPF não encontrado"}
        
        except Exception as e:
            return {"status": "error", "message": f"Erro ao buscar CPF: {str(e)}"}
        finally:
            conn.close()
    
    def buscar_cruzada(self, **kwargs):
        """Busca cruzada por múltiplos campos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Construir query dinamicamente
            condicoes = []
            valores = []
            
            for campo, valor in kwargs.items():
                if valor and campo in ['cpf', 'nome', 'rg', 'cnh', 'email', 'telefone', 'titulo_eleitor', 'pis', 'cns']:
                    if campo == 'nome':
                        condicoes.append(f"{campo} LIKE ?")
                        valores.append(f"%{valor}%")
                    else:
                        condicoes.append(f"{campo} = ?")
                        valores.append(valor)
            
            if not condicoes:
                return {"status": "error", "message": "Nenhum critério de busca fornecido"}
            
            query = f"SELECT * FROM pessoas WHERE {' OR '.join(condicoes)}"
            cursor.execute(query, valores)
            resultados = cursor.fetchall()
            
            pessoas_encontradas = []
            for resultado in resultados:
                pessoas_encontradas.append({
                    "id": resultado[0],
                    "cpf": resultado[1],
                    "nome": resultado[2],
                    "rg": resultado[3],
                    "cnh": resultado[4],
                    "email": resultado[5],
                    "telefone": resultado[6],
                    "titulo_eleitor": resultado[7],
                    "pis": resultado[8],
                    "cns": resultado[9],
                    "data_criacao": resultado[10],
                    "data_atualizacao": resultado[11]
                })
            
            return {
                "status": "success",
                "total_encontrados": len(pessoas_encontradas),
                "dados": pessoas_encontradas
            }
        
        except Exception as e:
            return {"status": "error", "message": f"Erro na busca cruzada: {str(e)}"}
        finally:
            conn.close()
    
    def inserir_dados_exemplo(self):
        """Insere dados de exemplo para teste"""
        dados_exemplo = [
            {
                "cpf": "12345678901",
                "nome": "João da Silva",
                "rg": "123456789",
                "cnh": "12345678901",
                "email": "joao.silva@email.com",
                "telefone": "11999999999",
                "titulo_eleitor": "123456789012",
                "pis": "12345678901",
                "cns": "123456789012345"
            },
            {
                "cpf": "98765432100",
                "nome": "Maria Santos",
                "rg": "987654321",
                "cnh": "98765432100",
                "email": "maria.santos@email.com",
                "telefone": "21888888888",
                "titulo_eleitor": "987654321098",
                "pis": "98765432100",
                "cns": "987654321098765"
            },
            {
                "cpf": "11122233344",
                "nome": "José da Conceição",
                "rg": "111222333",
                "cnh": "11122233344",
                "email": "jose.conceicao@email.com",
                "telefone": "31777777777",
                "titulo_eleitor": "111222333444",
                "pis": "11122233344",
                "cns": "111222333444555"
            }
        ]
        
        resultados = []
        for pessoa in dados_exemplo:
            resultado = self.inserir_pessoa(**pessoa)
            resultados.append(resultado)
        
        return resultados