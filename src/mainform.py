#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Created on 22.12.2010

@author: dik
'''

import pygtk
pygtk.require('2.0')
import gtk
import flbase

class MainForm(gtk.Builder):
    """classdocs"""

    def __init__(self):
        """Constructor"""
        super(MainForm, self).__init__()
        self.add_from_file("data/ui.glade")
        self.connect_signals(self)
        self.varts = self.get_object("treestore1")
        self.vars = []
        self.vc = 0
        self.tc = 0
        self.flb = flbase.FuzzyLogicBase()
        
        
    def main(self):
        gtk.main()
        
    def on_window1_destroy(self, _):
        gtk.main_quit()
        
    def on_add_button_clicked(self, _):
        self.get_object("t_entry1").set_text("var_" + str(self.vc))
        self.get_object("t_entry2").set_text("var_" + str(self.vc))
        self.get_object("a_entry").set_text("0")
        self.get_object("b_entry").set_text("0")
        self.get_object("c_entry").set_text("0")
        self.get_object("d_entry").set_text("0")
        self.get_object("dialog1").run()
        
    def on_del_button_clicked(self, _):
        cur, _ = self.get_object("treeview2").get_cursor()
        print cur
        
    def on_gen_button_clicked(self, _):
#        self.flb.print_base()
        self.flb.build_pr()
        self.flb.build_minpr()
        self.get_object("liststore3").clear()
        for i, st in enumerate(self.flb._prt):
            self.get_object("liststore3").append(row=[i + 1, st])
        for i, st in enumerate(self.flb._minprt):
            self.get_object("liststore5").append(row=[st, i + 1])
        self.get_object("status").set_text("Статус: Генерация закончена")
    
    def on_button_add_t_clicked(self, _):
        self.vars.append([None, []])
        self.flb.add_var(self.get_object("t_entry1").get_text(), self.get_object("t_entry2").get_text(), self.get_object("t_combobox").get_active())
        self.vars[len(self.vars) - 1][0] = self.varts.append(parent=None, row=[self.get_object("t_entry1").get_text(), self.get_object("t_entry2").get_text(), self.get_object("t_combobox").get_active_text()])
        self.get_object("liststore1").append(row=[self.get_object("t_entry1").get_text()])
        self.vc += 1
        if self.get_object("gen_term_checkbutton1").get_active():
            termc = int(self.get_object("spinbutton1").get_value())
            for _ in xrange(0, termc):
                function=self.get_object("fp_combobox1").get_active()
                if function == 0:
                    self.flb.add_term(self.get_object("t_entry1").get_text(), "term_" + str(self.tc), "term_" + str(self.tc), function, a=float(self.get_object("a_entry").get_text()), b=float(self.get_object("b_entry").get_text()), c=float(self.get_object("c_entry").get_text()))
                elif function == 1:
                    self.flb.add_term(self.get_object("t_entry1").get_text(), "term_" + str(self.tc), "term_" + str(self.tc), function, a=float(self.get_object("a_entry").get_text()), b=float(self.get_object("b_entry").get_text()), c=float(self.get_object("c_entry").get_text()), d=float(self.get_object("d_entry").get_text()))
                elif function == 2:
                    self.flb.add_term(self.get_object("t_entry1").get_text(), "term_" + str(self.tc), "term_" + str(self.tc), function, b=float(self.get_object("b_entry").get_text()), c=float(self.get_object("c_entry").get_text()))
                elif function == 3:
                    self.flb.add_term(self.get_object("t_entry1").get_text(), "term_" + str(self.tc), "term_" + str(self.tc), function, a=float(self.get_object("a_entry").get_text()))
                elif function == 4:
                    self.flb.add_term(self.get_object("t_entry1").get_text(), "term_" + str(self.tc), "term_" + str(self.tc), function, a=float(self.get_object("a_entry").get_text()), b=float(self.get_object("b_entry").get_text()), c=float(self.get_object("c_entry").get_text()))
                self.vars[len(self.vars) - 1][1].append(self.varts.append(self.vars[len(self.vars) - 1][0], ["term_" + str(self.tc), "term_" + str(self.tc), None]))
                self.tc += 1
        self.get_object("dialog1").hide()
    
    def on_button_add_term_clicked(self, _):
        function = self.get_object("fp_combobox2").get_active()
        tf = self.get_object("term_combobox1").get_active_text()
        tn = self.get_object("term_entry1").get_text()
        tn2 = self.get_object("term_entry2").get_text()
        if function == 0:
            self.flb.add_term(tf, tn, tn2, function, a=float(self.get_object("a_entry2").get_text()), b=float(self.get_object("b_entry2").get_text()), c=float(self.get_object("c_entry2").get_text()))
        elif function == 1:
            self.flb.add_term(tf, tn, tn2, function, a=float(self.get_object("a_entry2").get_text()), b=float(self.get_object("b_entry2").get_text()), c=float(self.get_object("c_entry2").get_text()), d=float(self.get_object("d_entry2").get_text()))
        elif function == 2:
            self.flb.add_term(tf, tn, tn2, function, b=float(self.get_object("b_entry2").get_text()), c=float(self.get_object("c_entry2").get_text()))
        elif function == 3:
            self.flb.add_term(tf, tn, tn2, function, a=float(self.get_object("a_entry2").get_text()))
        elif function == 4:
            self.flb.add_term(tf, tn, tn2, function, a=float(self.get_object("a_entry2").get_text()), b=float(self.get_object("b_entry").get_text()), c=float(self.get_object("c_entry").get_text()))
        self.vars[self.get_object("term_combobox1").get_active()][1].append(self.varts.append(self.vars[self.get_object("term_combobox1").get_active()][0], [self.get_object("term_entry1").get_text(), self.get_object("term_entry2").get_text(), None]))
        self.tc += 1
        self.get_object("dialog2").hide()
    
    def on_button_cancel_t_clicked(self, _):
        self.get_object("dialog1").hide()
    
    def on_button_cancel_term_clicked(self, _):
        self.get_object("dialog2").hide()
        
    def on_add_term_button_clicked(self, _):
        cur, _ = self.get_object("treeview2").get_cursor()
        if cur != None:
            self.get_object("term_combobox1").set_active(cur[0])
            self.get_object("term_entry1").set_text("term_" + str(self.tc))
            self.get_object("term_entry2").set_text("term_" + str(self.tc))
            self.get_object("a_entry2").set_text("0")
            self.get_object("b_entry2").set_text("0")
            self.get_object("c_entry2").set_text("0")
            self.get_object("d_entry2").set_text("0")
            self.get_object("dialog2").run()
        
    def on_edit_button_clicked(self, _):
        pass
    
    def on_treeview2_row_activated(self, a, b, c):
        pass
        
    def on_fp_combobox1_changed(self, _):
        fp = self.get_object("fp_combobox1").get_active()
        if fp == 0:
            self.get_object("a_label").props.visible = True
            self.get_object("b_label").props.visible = True
            self.get_object("c_label").props.visible = True
            self.get_object("d_label").props.visible = False
            self.get_object("a_entry").props.editable = True
            self.get_object("a_entry").props.visible = True
            self.get_object("b_entry").props.editable = True
            self.get_object("b_entry").props.visible = True
            self.get_object("c_entry").props.editable = True
            self.get_object("c_entry").props.visible = True
            self.get_object("d_entry").props.editable = False
            self.get_object("d_entry").props.visible = False
        elif fp == 1:
            self.get_object("a_label").props.visible = True
            self.get_object("b_label").props.visible = True
            self.get_object("c_label").props.visible = True
            self.get_object("d_label").props.visible = True
            self.get_object("a_entry").props.editable = True
            self.get_object("a_entry").props.visible = True
            self.get_object("b_entry").props.editable = True
            self.get_object("b_entry").props.visible = True
            self.get_object("c_entry").props.editable = True
            self.get_object("c_entry").props.visible = True
            self.get_object("d_entry").props.editable = True
            self.get_object("d_entry").props.visible = True
        elif fp == 2:
            self.get_object("a_label").props.visible = False
            self.get_object("b_label").props.visible = True
            self.get_object("c_label").props.visible = True
            self.get_object("d_label").props.visible = False
            self.get_object("a_entry").props.editable = False
            self.get_object("a_entry").props.visible = False
            self.get_object("b_entry").props.editable = True
            self.get_object("b_entry").props.visible = True
            self.get_object("c_entry").props.editable = True
            self.get_object("c_entry").props.visible = True
            self.get_object("d_entry").props.editable = False
            self.get_object("d_entry").props.visible = False
        elif fp == 3:
            self.get_object("a_label").props.visible = True
            self.get_object("b_label").props.visible = False
            self.get_object("c_label").props.visible = False
            self.get_object("d_label").props.visible = False
            self.get_object("a_entry").props.editable = True
            self.get_object("a_entry").props.visible = True
            self.get_object("b_entry").props.editable = False
            self.get_object("b_entry").props.visible = False
            self.get_object("c_entry").props.editable = False
            self.get_object("c_entry").props.visible = False
            self.get_object("d_entry").props.editable = False
            self.get_object("d_entry").props.visible = False
        elif fp == 4:
            self.get_object("a_label").props.visible = True
            self.get_object("b_label").props.visible = True
            self.get_object("c_label").props.visible = True
            self.get_object("d_label").props.visible = False
            self.get_object("a_entry").props.editable = True
            self.get_object("a_entry").props.visible = True
            self.get_object("b_entry").props.editable = True
            self.get_object("b_entry").props.visible = True
            self.get_object("c_entry").props.editable = True
            self.get_object("c_entry").props.visible = True
            self.get_object("d_entry").props.editable = False
            self.get_object("d_entry").props.visible = False
        else:
            print "Error, fp doesn't exist."
    
    def on_fp_combobox2_changed(self, _):
        fp = self.get_object("fp_combobox2").get_active()
        if fp == 0:
            self.get_object("a_label2").props.visible = True
            self.get_object("b_label2").props.visible = True
            self.get_object("c_label2").props.visible = True
            self.get_object("d_label2").props.visible = False
            self.get_object("a_entry2").props.editable = True
            self.get_object("a_entry2").props.visible = True
            self.get_object("b_entry2").props.editable = True
            self.get_object("b_entry2").props.visible = True
            self.get_object("c_entry2").props.editable = True
            self.get_object("c_entry2").props.visible = True
            self.get_object("d_entry2").props.editable = False
            self.get_object("d_entry2").props.visible = False
        elif fp == 1:
            self.get_object("a_label2").props.visible = True
            self.get_object("b_label2").props.visible = True
            self.get_object("c_label2").props.visible = True
            self.get_object("d_label2").props.visible = True
            self.get_object("a_entry2").props.editable = True
            self.get_object("a_entry2").props.visible = True
            self.get_object("b_entry2").props.editable = True
            self.get_object("b_entry2").props.visible = True
            self.get_object("c_entry2").props.editable = True
            self.get_object("c_entry2").props.visible = True
            self.get_object("d_entry2").props.editable = True
            self.get_object("d_entry2").props.visible = True
        elif fp == 2:
            self.get_object("a_label2").props.visible = False
            self.get_object("b_label2").props.visible = True
            self.get_object("c_label2").props.visible = True
            self.get_object("d_label2").props.visible = False
            self.get_object("a_entry2").props.editable = False
            self.get_object("a_entry2").props.visible = False
            self.get_object("b_entry2").props.editable = True
            self.get_object("b_entry2").props.visible = True
            self.get_object("c_entry2").props.editable = True
            self.get_object("c_entry2").props.visible = True
            self.get_object("d_entry2").props.editable = False
            self.get_object("d_entry2").props.visible = False
        elif fp == 3:
            self.get_object("a_label2").props.visible = True
            self.get_object("b_label2").props.visible = False
            self.get_object("c_label2").props.visible = False
            self.get_object("d_label2").props.visible = False
            self.get_object("a_entry2").props.editable = True
            self.get_object("a_entry2").props.visible = True
            self.get_object("b_entry2").props.editable = False
            self.get_object("b_entry2").props.visible = False
            self.get_object("c_entry2").props.editable = False
            self.get_object("c_entry2").props.visible = False
            self.get_object("d_entry2").props.editable = False
            self.get_object("d_entry2").props.visible = False
        elif fp == 4:
            self.get_object("a_label2").props.visible = True
            self.get_object("b_label2").props.visible = True
            self.get_object("c_label2").props.visible = True
            self.get_object("d_label2").props.visible = False
            self.get_object("a_entry2").props.editable = True
            self.get_object("a_entry2").props.visible = True
            self.get_object("b_entry2").props.editable = True
            self.get_object("b_entry2").props.visible = True
            self.get_object("c_entry2").props.editable = True
            self.get_object("c_entry2").props.visible = True
            self.get_object("d_entry2").props.editable = False
            self.get_object("d_entry2").props.visible = False
        else:
            print "Error, fp doesn't exist."
            
    def on_imagemenuitem3_activate(self, _):
        self.get_object("filechooserdialog1").run()
    
    def on_sv_cancel_clicked(self, _):
        self.get_object("filechooserdialog1").hide()
        
    def on_sv_save_clicked(self, _):
        fln = self.get_object("filechooserdialog1").get_filename()
        f = file(fln, "wb")
        params = {}
        params['Name'] = 'test'
        params['Type'] = 'madmani'
        params['Version'] = 2.0
        params['NumInputs'], params['NumOutputs'] = self.flb.get_counts()
        params['NumRules'] = len(self.flb._minpr)
        params['AndMethod'] = 'min'
        params['OrMethod'] = 'max'
        params['ImpMethod'] = 'min'
        params['AggMethod'] = 'max'
        params['DefuzzMethod'] = 'centroid'
        
        params['Inputs'] = self.flb.get_inputs_matcad()
        params['Outputs'] = self.flb.get_outputs_matcad()
        
        params['Rules'] = self.flb.get_rules()
        
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
        
        self.get_object("filechooserdialog1").hide()
   
        
if __name__ == "__main__":
    pr = MainForm()
    pr.main()
