/*
This file is part of PyMbs.

PyMbs is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PyMbs is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public 
License along with PyMbs.
If not, see <http://www.gnu.org/licenses/>.

Copyright 2011, 2012 Carsten Knoll, Christian Schubert, 
                     Jens Frenkel, Sebastian Voigt
*/

#include "CNumber.h"
#include "CBasic.h"
#include "SymbolicsError.h"
#include "convert.h"

using namespace Symbolics::Python;

#pragma region CNumber

// Konstruktor
static int CNumber_init(CNumberObject *self, PyObject *args, PyObject *kwds);
static void CNumber_del(CNumberObject *self);

// Dokumentation
static char CNumber_doc[] = 
    "Number, directly implemented in C++";

// TypeObject
PyTypeObject Symbolics::Python::CNumberObjectType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"symbolics.Number",           /* tp_name           */
    sizeof(CNumberObject),        /* tp_basicsize      */
    0,                            /* tp_itemsize       */
    0,                            /* tp_dealloc        */
    0,                            /* tp_print          */
    0,                            /* tp_getattr        */
    0,                            /* tp_setattr        */
    0,                            /* tp_compare        */
    0,                            /* tp_repr           */
    0,                            /* tp_as_number      */
    0,                            /* tp_as_sequence    */
    0,                            /* tp_as_mapping     */
    0,                            /* tp_hash           */
    0,                            /* tp_call           */
    0,                            /* tp_str            */
    0,                            /* tp_getattro       */
    0,                            /* tp_setattro       */
    0,                            /* tp_as_buffer      */
    Py_TPFLAGS_DEFAULT,           /* tp_flags          */
    CNumber_doc,                  /* tp_doc            */
    0,                            /* tp_traverse       */
    0,                            /* tp_clear          */
    0,                            /* tp_richcompare    */
    0,                            /* tp_weaklistoffset */
    0,                            /* tp_iter           */
    0,                            /* tp_iternext       */
    0,                             /* tp_methods        */
    0,                            /* tp_members        */
    0,                            /* tp_getset         */
    &CBasicObjectType,            /* tp_base           */
    0,                            /* tp_dict           */
    0,                            /* tp_descr_get      */
    0,                            /* tp_descr_set      */
    0,                            /* tp_dictoffset     */
    (initproc)CNumber_init,        /* tp_init           */
    0,                            /* tp_alloc          */
    0,                            /* tp_new            */
    0,                            /* tp_free           */
    0,                            /* tp_is_gc          */
    0,                            /* tp_bases          */
    0,                            /* tp_mro            */
    0,                            /* tp_cache          */
    0,                            /* tp_subclasses     */
    0,                            /* tp_weaklist       */
    (destructor)CNumber_del,    /* tp_del            */
};
#pragma endregion

#pragma region CNumber
// Konstruktor
/*****************************************************************************/
static int CNumber_init(CNumberObject *self, PyObject *args, PyObject *kwds)
/*****************************************************************************/
{
    try
    {
        // Args = (exp)
        if (!PyTuple_Check(args))
        {
            PyErr_SetString(SymbolicsError, "args must be a tuple!");
            return -1;
        }
         size_t nArgs = PyTuple_Size(args);
        if (nArgs > 1)
        {
            PyErr_SetString(SymbolicsError, "len(args) must not exceed one, i.e. Number(expression)!");
            return -1;
        }
        if (nArgs < 1)
        {
            PyErr_SetString(SymbolicsError, "len(args) must be at least one, i.e. Number(expression)!");
            return -1;
        }
        // Expression extrahieren
		PyObject *item = PyTuple_GetItem(args, 0);

		// Ist es ein Int?
		if (PyLong_Check(item))
			self->m_basic = Int::New( PyLong_AsLong(item) );
		else if (PyFloat_Check(item))
			self->m_basic = BasicPtr( new Real( PyFloat_AsDouble(item) ) );
		else
		{
			PyErr_SetString(SymbolicsError, "Argument must be either int or float!");
			return -1;
		}
    }
	STD_ERROR_HANDLER(-1);

    return 0;
}
/*****************************************************************************/

// Destruktor
/*****************************************************************************/
static void CNumber_del(CNumberObject *self)
/*****************************************************************************/
{
    // Referenz loeschen, boost::intrusive_ptr kuemmert sich um den Rest
    self->m_basic = NULL;
}
/*****************************************************************************/

#pragma endregion

