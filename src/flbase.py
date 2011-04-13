#-*- coding: utf-8 -*-
"""
Created on 15.01.2011

@author: dik
"""

import math

InVar = 0
OutVar = 1

class FuzzyLogicBase(object):
    """classdocs
    """
    
    _base = {}
    _pr = []
    hasOut = False
    mX = 0
    mY = 0
    
    def __init__(self):
        """Constructor
        """
        pass
    
    def add_var(self, name, description, type=InVar):
        """Добаляет переменныю в базу, каждая переменная должна содержать
        набор термов добавляемых через add_term
        """
        if name in self._base.keys():
            print "Variable", name, """already exists. Please rename or delete existing variable before continue."""
        elif type == InVar or type == OutVar:
            if type == InVar or (type == OutVar and self.hasOut == False):
                self._base[name] = {'description':description, 'type': type, 'terms':{}, 'termc': 0}
                if type == OutVar:    
                    self.hasOut = True
            else:
                print "Out Variable already exist."
        else:
            print "Unrecognized type"
        
    def add_term(self, pvname, termname, termdesc, function=0, **params):
        """Добавляет терм в определенную переменную
        """
        if pvname not in self._base.keys():
            print "Parent varialbe does not exist."
        elif termname in self._base[pvname]['terms'].keys():
            print "Term already exist."
        else:
            self._base[pvname]['termc'] += 1 
            if function == 0:
                center = self.triangle_c(params['a'], params['b'], params['c'])
                self._base[pvname]['terms'][termname] = {'termdesc':termdesc, 'f':function, 'a':params['a'], 'b':params['b'], 'c':params['c'], 'center':center}
            elif function == 1:
                center = self.trapeze_c(params['a'], params['b'], params['c'], params['d'])
                self._base[pvname]['terms'][termname] = {'termdesc':termdesc, 'f':function, 'a':params['a'], 'b':params['b'], 'c':params['c'], 'd':params['d'], 'center':center}
            elif function == 2:
                center = self.gauss_c(params['b'], params['c'])
                self._base[pvname]['terms'][termname] = {'termdesc':termdesc, 'f':function, 'b':params['b'], 'c':params['c'], 'center':center}
            elif function == 3:
                center = self.singleton_c(params['a'])
                self._base[pvname]['terms'][termname] = {'termdesc':termdesc, 'f':function, 'a':params['a'], 'center':center}
            elif function == 4:
                center = self.bell_c(params['a'], params['b'], params['c'])
                self._base[pvname]['terms'][termname] = {'termdesc':termdesc, 'f':function, 'a':params['a'], 'b':params['b'], 'c':params['c'], 'center':center}
            else:
                print "Unknown function"
            self._base[pvname]['terms'][termname]['termnum'] = self._base[pvname]['termc']
    
    def del_var(self, name):
        """Удаляет переменную и все принадлежащие ей термы
        """
        del(self._base[name])
    
    def del_term(self, pvname, termname):
        """Удаляет определенный терм из переменной
        """
        del(self._base[pvname]['terms'][termname])
    
    def print_base(self):
        """Отладочный вывод
        """
        for key in self._base:
            print key, ":", self._base[key]
    
    def build_pr(self):
        """Генерация полного покрытия
        """
        import itertools
        inMas = []
        outMas = []
        temp = []
        # генерим плоские представления функций
        for var in sorted(self._base):
            if self._base[var]['type'] == OutVar:
                for term in sorted(self._base[var]['terms']):
                    outMas.append([var, term])
            else:
                for term in sorted(self._base[var]['terms']):
                    temp.append([var, term])
                inMas.append(temp)
                temp = []
        
        inMasX = list(itertools.product(*inMas))
        self.mX, self.mY = len(inMasX), len(outMas)
#        if len(inMas) == 0:
#            pass
#        elif len(inMas) == 1:
#            pass
#        elif len(inMas) == 2:
#            inMasX = list(itertools.product(inMas[0], inMas[1]))
#        elif len(inMas) > 2:
#            inMasX = list(itertools.product(inMas[0], inMas[1]))
#            for n, i in enumerate(inMas):
#                if n >= 2:
#                    inMasX = list(itertools.product(inMasX, inMas[n]))
#                    inMasX = map(lambda x: x[0] + (x[1], ), inMasX)
        
#        print inMasX
        
        outMasX = []
        temp = []
        for var in sorted(inMasX):
            for par in sorted(outMas):
                outMasX.append([var, par])
        
        self._pr = outMasX
        stringMas = []
        temp = ""
        
        for i in sorted(outMasX):
            for n in i[0]:
                temp += self._base[n[0]]['description'] + " " 
                temp += self._base[n[0]]['terms'][n[1]]['termdesc'] + " & "
            temp = temp[:-3]
            temp = temp + " => " + self._base[i[1][0]]['description'] + " " + self._base[i[1][0]]['terms'][i[1][1]]['termdesc']
            stringMas.append(temp)
            temp = ""
        self._prt = stringMas
        
    def triangle(self, u, a, b, c):
        u = float(u)
        a = float(a)
        b = float(b)
        c = float(c)
        if (a >= u) or (u >= c):
            return 0
        elif a < u <= b:
            return (u - a) / (b - a)
        elif b < u < c:
            return (c - u) / (c - b)
        else:
            return -1
    
    def triangle_c(self, a, b, c):
        return b
    
    def trapeze(self, u, a, b, c, d):
        u = float(u)
        a = float(a)
        b = float(b)
        c = float(c)
        d = float(d)
        if (a >= u) or (u >= d):
            return 0
        elif a <= u <= b:
            return (u - a) / (b - a)
        elif b <= u <= c:
            return 1
        elif c <= u <= d:
            return (d - u) / (d - c)
        
    def trapeze_c(self, a, b, c, d):
        return (c + b) / 2.0
    
    def gauss(self, u, b, c):
        u = float(u)
        b = float(b)
        c = float(c)
        return math.exp(-((u - b)**2 / (2*c)**2))
    
    def gauss_c(self, b, c):
        return b
    
    def singleton(self, u, a):
        u = float(u)
        a = float(a)
        if u == a:
            return 1
        else:
            return 0
        
    def singleton_c(self, a):
        return a
    
    def bell(self, u, a, b, c):
        u = float(u)
        a = float(a)
        b = float(b)
        c = float(c)
        return 1.0 / (1 + ((u - c) / a)**(2*b))
    
    def bell_c(self, a, b, c):
        return c
    
    def create_matrix2d(self, x, y, c):
        temp = []
        for i in xrange(0, x):
            temp.append([])
            for _ in xrange(0, y):
                temp[i].append(c)
        return temp
        
    def build_minpr(self):
        self._tnorm = []
        self._otkl = self.create_matrix2d(self.mX, self.mY, 0)
        self._alpha = []
        self._alphax = []
        self._minpr = []
        for i in self._pr:
            self._tnorm.append(1)
            for n in i[0]:
                self._tnorm[len(self._tnorm) - 1] *= self._base[n[0]]['terms'][n[1]]['center']
                
        list.sort(self._tnorm)
        
        lx = -1
        for _, i in enumerate(self._base):
            if self._base[i]['type'] == 1:
                lx = i
                break
        
        for i in xrange(0, self.mX):
            for name in sorted(self._base[lx]['terms']):
                tmp = self._base[lx]['terms'][name]['termnum']
                print i, self.mX, tmp, len(self._tnorm), tmp*i, self.mY*i + tmp - 1
                self._otkl[i][tmp - 1] = abs(self._tnorm[self.mY*i + tmp - 1] - self._base[lx]['terms'][name]['center'])
        
        for i in sorted(self._base[lx]['terms']):
            self._alphax.append(self._base[lx]['terms'][i]['center'])
            
        list.sort(self._alphax)
        print self._alphax
        
        for i in xrange(0, len(self._alphax) - 1):
            self._alpha.append(abs(self._alphax[i + 1] - self._alphax[i]) / 2.0)
        self._alpha.append(abs(self._alphax[len(self._alphax) - 1] - 1.0) / 2.0)
        
        print self._alpha
        print self._pr
        
        for i in xrange(0, len(self._otkl)):
            for j in xrange(0, len(self._alpha)):
                if self._otkl[i][j] <= self._alpha[j]:
                    self._minpr.append(self._pr[i*len(self._alpha) + j])
        
        print "T-норма", len(self._tnorm), self._tnorm
        print "Отклонение", len(self._otkl), self._otkl
        print "Альфа-сечение", len(self._alpha), self._alpha
        print "Минимальное покрытие", len(self._minpr), self._minpr
        
        stringMas = []
        temp = ""
        
        for i in self._minpr:
            for n in i[0]:
                temp += self._base[n[0]]['description'] + " " + self._base[n[0]]['terms'][n[1]]['termdesc'] + " & "
            temp = temp[:-3]
            temp = temp + " => " + self._base[i[1][0]]['description'] + " " + self._base[i[1][0]]['terms'][i[1][1]]['termdesc']
            stringMas.append(temp)
            temp = ""
        print len(stringMas), stringMas
        for i in stringMas:
            print i
        self._minprt = stringMas
    
    def get_counts(self):
        inp = 0
        out = 0
        for key in self._base.keys():
            if self._base[key]['type'] == 0:
                inp += 1
            else:
                out += 1
        return inp, out
    
    def get_inputs_matcad(self):
        out = {}
        i = 0
        for key in self._base.keys():
            if self._base[key]['type'] == 0:
                i += 1
                out['Input' + str(i)] = {}
                out['Input' + str(i)]['Name'] = self._base[key]['description']
                out['Input' + str(i)]['Range'] = [0, 1] #TODO: Заглушка поправить
                out['Input' + str(i)]['NumMFs'] = len(self._base[key]['terms'])
                out['Input' + str(i)]['MFs'] = {}
                keys = self._base[key]['terms'].keys()
                keys.sort()
                for j, term in enumerate(keys):
                    if self._base[key]['terms'][term]['f'] == 0:
                        out['Input' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "trimf", [self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['b'], self._base[key]['terms'][term]['c']]]
                    elif self._base[key]['terms'][term]['f'] == 1:
                        out['Input' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "trapmf", [self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['b'], self._base[key]['terms'][term]['c'], self._base[key]['terms'][term]['d']]]
                    elif self._base[key]['terms'][term]['f'] == 2:
                        out['Input' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "gaussmf", [self._base[key]['terms'][term]['b'], self._base[key]['terms'][term]['c']]]
                    elif self._base[key]['terms'][term]['f'] == 3:
                        out['Input' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "trapmf", [self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['a']]]
                    elif self._base[key]['terms'][term]['f'] == 4:
                        out['Input' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "gbellmf", [self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['b'], self._base[key]['terms'][term]['c']]]
        return out
    
    def get_outputs_matcad(self):
        out = {}
        i = 0
        for key in self._base.keys():
            if self._base[key]['type'] == 1:
                i += 1
                out['Output' + str(i)] = {}
                out['Output' + str(i)]['Name'] = self._base[key]['description']
                out['Output' + str(i)]['Range'] = [0, 1] #TODO: Заглушка поправить
                out['Output' + str(i)]['NumMFs'] = len(self._base[key]['terms'])
                out['Output' + str(i)]['MFs'] = {}
                keys = self._base[key]['terms'].keys()
                keys.sort()
                for j, term in enumerate(keys):
                    if self._base[key]['terms'][term]['f'] == 0:
                        out['Output' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "trimf", [self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['b'], self._base[key]['terms'][term]['c']]]
                    elif self._base[key]['terms'][term]['f'] == 1:
                        out['Output' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "trapmf", [self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['b'], self._base[key]['terms'][term]['c'], self._base[key]['terms'][term]['d']]]
                    elif self._base[key]['terms'][term]['f'] == 2:
                        out['Output' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "gaussmf", [self._base[key]['terms'][term]['b'], self._base[key]['terms'][term]['c']]]
                    elif self._base[key]['terms'][term]['f'] == 3:
                        out['Output' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "trapmf", [self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['a']]]
                    elif self._base[key]['terms'][term]['f'] == 4:
                        out['Output' + str(i)]['MFs']['MF' + str(j + 1)] = [self._base[key]['terms'][term]['termdesc'], "gbellmf", [self._base[key]['terms'][term]['a'], self._base[key]['terms'][term]['b'], self._base[key]['terms'][term]['c']]]
        return out
    
    def get_rules(self):
        out = []
        tmp = ""
        for [inv, outv] in self._minpr:
            tmp = ""
            for pr in inv:
                print inv, self._base[pr[0]]['terms'][pr[1]]['termnum']
                tmp += str(self._base[pr[0]]['terms'][pr[1]]['termnum']) + " "
            tmp = tmp[:-1] + ", "
            tmp += str(self._base[outv[0]]['terms'][outv[1]]['termnum']) + " "
            tmp = tmp[:-1] + " (1) : 1"
            out.append(tmp)
        return out
		
    def save_to_file(self, fln):
    	f = file(fln, "wb")
        params = {}
        params['Name'] = 'test'
        params['Type'] = 'madmani'
        params['Version'] = 2.0
        params['NumInputs'], params['NumOutputs'] = self.get_counts()
        params['NumRules'] = len(self._minpr)
        params['AndMethod'] = 'min'
        params['OrMethod'] = 'max'
        params['ImpMethod'] = 'min'
        params['AggMethod'] = 'max'
        params['DefuzzMethod'] = 'centroid'
        
        params['Inputs'] = self.get_inputs_matcad()
        params['Outputs'] = self.get_outputs_matcad()
        
        params['Rules'] = self.get_rules()
        
        f.write("[System]\nName='" + params['Name'] + "'\nType='" + params['Type'] +
                "'\nVersion=" + str(params['Version']) + "\nNumInputs=" + str(params['NumInputs']) +
                "\nNumOutputs=" + str(params['NumOutputs']) + "\nNumRules=" + str(params['NumRules']) +
                "\nAndMethod='" + params['AndMethod'] + "'\nOrMethod='" + params['OrMethod'] +
                "'\nImpMethod='" + params['ImpMethod'] + "'\nAggMethod='" + params['AggMethod'] +
                "'\nDefuzzMethod='" + params['DefuzzMethod'] + "'\n\n")
        
        keys = params['Inputs'].keys()
        keys.sort()
        for key in keys:
            f.write("[" + key + "]\nName='" + params['Inputs'][key]['Name'] + "'\nRange=[0 1]" + "\nNumMFs=" + str(params['Inputs'][key]['NumMFs']) + "\n")
            fkeys = params['Inputs'][key]['MFs'].keys()
            fkeys.sort()
            for fkey in fkeys:
                f.write(fkey + "='" + params['Inputs'][key]['MFs'][fkey][0] + "':'" + params['Inputs'][key]['MFs'][fkey][1] + "',")
                tmp = "["
                for ff in params['Inputs'][key]['MFs'][fkey][2]:
                    tmp += str(ff) + " "
                tmp = tmp[:-1] + "]"
                f.write(tmp + "\n")
            f.write("\n")
                
        keys = params['Outputs'].keys()
        keys.sort()
        for key in keys:
            f.write("[" + key + "]\nName='" + params['Outputs'][key]['Name'] + "'\nRange=[0 1]" + "\nNumMFs=" + str(params['Outputs'][key]['NumMFs']) + "\n")
            fkeys = params['Outputs'][key]['MFs'].keys()
            fkeys.sort()
            for fkey in fkeys:
                f.write(fkey + "='" + params['Outputs'][key]['MFs'][fkey][0] + "':'" + params['Outputs'][key]['MFs'][fkey][1] + "',")
                tmp = "["
                for ff in params['Outputs'][key]['MFs'][fkey][2]:
                    tmp += str(ff) + " "
                tmp = tmp[:-1] + "]"
                f.write(tmp + "\n")
            f.write("\n")   
        
        f.write("[Rules]\n")
        
        for rule in params['Rules']:
            f.write(rule + "\n")
                             
if __name__ == "__main__":
    flb = FuzzyLogicBase()
    
    flb.add_var("inVar1", "расстояние", type=InVar)
    flb.add_var("inVar2", "угол", type=InVar)
    flb.add_var("outer", "мощность", type=OutVar)
    flb.add_term("inVar1", "in11", "очень далекое", function=1, a=0, b=0, c=0.125, d=0.25)
    flb.add_term("inVar1", "in12", "ноль", function=0, a=0.125, b=0.25, c=0.375)
    flb.add_term("inVar1", "in13", "близкое", function=0, a=0.25, b=0.375, c=0.5)
    flb.add_term("inVar1", "in14", "среднее", function=0, a=0.375, b=0.5, c=0.8)
    flb.add_term("inVar1", "in15", "далекое", function=1, a=0.5, b=0.8, c=1, d=1)
    flb.add_term("inVar2", "in21", "отр_большой", function=1, a=0, b=0, c=0.21875, d=0.46875)
    flb.add_term("inVar2", "in22", "отр_малый", function=0, a=0.21875, b=0.46875, c=0.5)
    flb.add_term("inVar2", "in23", "ноль", function=0, a=0.46875, b=0.5, c=0.53125)
    flb.add_term("inVar2", "in24", "пол_малый", function=0, a=0.5, b=0.53125, c=0.78125)
    flb.add_term("inVar2", "in25", "пол_большой", function=1, a=0.53125, b=0.78125, c=1, d=1)
    flb.add_term("outer", "out11", "отр_высока", function=3, a=0)
    flb.add_term("outer", "out12", "отр_средняя", function=3, a=0.27)
    flb.add_term("outer", "out13", "ноль", function=3, a=0.5)
    flb.add_term("outer", "out14", "пол_средняя", function=3, a=0.72)
    flb.add_term("outer", "out15", "пол_высокая", function=3, a=1)
    
#    flb.add_var("inVar1", "температура", type=InVar)
#    flb.add_var("outer", "угол поворота", type=OutVar)
#    flb.add_term("inVar1", "in11", "горячая", function=1, a=0, b=0, c=0.1, d=0.3)
#    flb.add_term("inVar1", "in12", "не очень горячая", function=0, a=0.2, b=0.35, c=0.5)
#    flb.add_term("inVar1", "in13", "теплая", function=0, a=0.4, b=0.5, c=0.6)
#    flb.add_term("inVar1", "in14", "прохладная", function=0, a=0.5, b=0.6, c=0.7)
#    flb.add_term("inVar1", "in15", "холодная", function=1, a=0.6, b=0.9, c=1, d=1)
#    flb.add_term("outer", "out11", "большой угол вправо", function=1, a=0, b=0, c=0.1, d=0.3)
#    flb.add_term("outer", "out12", "небольшой угол вправо", function=0, a=0.2, b=0.35, c=0.5)
#    flb.add_term("outer", "out13", "нуль", function=0, a=0.4, b=0.5, c=0.6)
#    flb.add_term("outer", "out14", "небольшой угол влево", function=0, a=0.5, b=0.65, c=0.8)
#    flb.add_term("outer", "out15", "большой угол влево", function=1, a=0.7, b=0.9, c=1, d=1)

    flb.print_base()
    flb.build_pr()
    flb.build_minpr()
    flb.save_to_file("1.fis")
#    print flb.get_counts()
#    print flb.get_inputs_matcad()
#    print flb.get_outputs_matcad()
#    flb.get_rules()
#    print flb.get_rules()