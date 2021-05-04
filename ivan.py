import argparse


parse = argparse.ArgumentParser()

parse.add_argument("FileIn" , help = "Srt file in to fix")
parse.add_argument("FileOut", help = "Name of file out(.srt)")
parse.add_argument("-v", "--verbose", help = "increase output verbosity", action = "store_true")
args = parse.parse_args()





class nodo():
    'Inicializamos la clase para poder organizar todo en su lugar respectivo, para poder comparar los tiempos'

    def __init__(self, Seq=0, StartTime="", EndTime="", Caption=""):
        self.pos = Seq
        self.TiempoStart = StartTime
        self.TiempoEnd = EndTime
        self.texto = []
        if Caption != '':
            self.texto.append(Caption)

    def Load(self, f):
        Linea = f.readline().rstrip("\n")
        if Linea:
            self.pos = int (Linea)
            tiempo = f.readline().rstrip("\n")
            self.TiempoStart = tiempo[1:12]
            self.TiempoEnd =  tiempo [17:]

            Linea = f.readline().rstrip("\n")
            while Linea != "":
                self.texto.append(Linea)
                Linea = f.readline().rstrip("\n")
            return True
        else:
            return False

    def save(self,fp):
        fp.write(f'{self.pos}\n')
        fp.write(f'{self.TiempoStart} --> {self.TiempoEnd}\n')
        for linea in self.texto:
            fp.write(linea + "\n")
        fp.write("\n")

    # Esto hace que la clase pueda ser tratada como un str

    def __repr__(self):
        return f'{self.TiempoStart} --> {self.TiempoEnd} {self.texto}'

    # Si los tiempos coinciden, esto hace que el texto del primer bloque se junte por el texto del siguiente

    def merge(self, nodo):
        self.texto = self.texto + nodo.texto
        return self.texto

    # Metodo para imprimir la clase

    def print_nodo(self):
        print (self.TiempoStart )
        print (self.TiempoEnd )
        print (self.texto )

    # Comprueba si los tiempos de los nodos son iguales para lanzar el Merge

    def is_mergeable(self, nodo):
        if self.TiempoStart == nodo.TiempoStart:
            return True
        else:
            return False

    # Crea la Lista de los nodos

def LoadLista(FileName):
    
    Lista = []

    with open(FileName,"rt") as fp:
        Status = True

        while Status == True:
            MyNode = nodo()
            Status = MyNode.Load(fp)
            if Status == True:
                Lista.append(MyNode)
    return Lista

    # Procesa la lista y hace uso de los metodos IsMergeable y Merge

def ProcesaLista(ListaIn, ListaOut):

    nodo1 = ListaIn.pop(0)

    if (nodo1):
        while ListaIn:
            nodo2 = ListaIn.pop(0)

            if nodo1.is_mergeable(nodo2):
                nodo1.merge(nodo2)
            else:
                nodo2.pos = nodo1.pos + 1
                ListaOut.append(nodo1)
                nodo1 = nodo2
        ListaOut.append(nodo1)

def SaveLista(Lista,FileName):
    with open(FileName,"wt") as fp:
        for Nodo in Lista:
            Nodo.save(fp)

def main():
    Lista = []
    ListaOut = []

    Lista = LoadLista(args.FileIn)

    ProcesaLista(Lista,ListaOut)
    SaveLista(ListaOut, args.FileOut)

main()