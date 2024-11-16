import { useFormik } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-hot-toast';

const MemberForm = ({ darkMode }) => {
    const formik = useFormik({
        initialValues: {
            firstName: '',
            lastName: '',
            DOB: '',
            location: '',
            phone: '',
            isStudent: false,
            school: '',
            isVisitor: false,
            willBeComing: false,
            occupation: '',
            group: '',
            leader: false,
            gender: '',
            emergencyContact: {
                name: '',
                phone: '',
                relation: ''
            },
        },
        validationSchema: Yup.object({
            firstName: Yup.string().required('Required'),
            lastName: Yup.string().required('Required'),
            DOB: Yup.date().required('Required'),
            location: Yup.string().required('Required'),
            // phone: Yup.string().required('Required'),
            // occupation: Yup.string().required('Required'),
            // group: Yup.string().required('Required'),
            // gender: Yup.string().required('Required'),
            emergencyContact: Yup.object({
                name: Yup.string().required('Required'),
                phone: Yup.string().required('Required'),
                relation: Yup.string().required('Required'),
            }),
        }),
        onSubmit: async (values, { setSubmitting, resetForm }) => {
            try {
                const newMember = {
                    first_name: values.firstName,
                    last_name: values.lastName,
                    dob: values.DOB,
                    location: values.location,
                    phone: values.phone,
                    leader: values.leader,
                    is_student: values.isStudent,
                    school: values.isStudent ? values.school : '',
                    is_visitor: values.isVisitor,
                    will_be_coming: values.isVisitor ? values.willBeComing : false,
                    occupation: values.occupation,
                    group_id: values.group,
                    gender_enum: values.gender,
                    emergency_contact_id: [ values.emergencyContact],
                };

                const response = await fetch('http://127.0.0.1:5000/adminregistry', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(newMember),
                });

                if (response.ok) {
                    toast.success('Member registered successfully!');
                    resetForm();
                } else {
                    const errorData = await response.json();
                    toast.error(`Failed to register member. ${errorData.error || 'Please try again.'}`);
                }
            } catch (err) {
                console.error(err);
                toast.error('An error occurred. Please try again later.');
            } finally {
                setSubmitting(false);
            }
        },
    });

    return (
        <div className={`min-h-screen p-4 font-sans flex justify-center items-center ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
            <div className={`w-full max-w-4xl mx-auto rounded-lg shadow-lg p-8 ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                <h1 className={`text-3xl font-semibold text-center ${darkMode ? 'text-gray-100' : 'text-gray-800'} mb-6`}>Register a New Member</h1>
                <form onSubmit={formik.handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <InputField formik={formik} name="firstName" label="First Name" darkMode={darkMode} />
                    <InputField formik={formik} name="lastName" label="Last Name" darkMode={darkMode} />
                    <RadioField formik={formik} name="gender" label="Gender" options={["Male", "Female"]} darkMode={darkMode} />
                    <InputField formik={formik} name="DOB" label="Date of Birth" type="date" darkMode={darkMode} />
                    <InputField formik={formik} name="location" label="Location" darkMode={darkMode} />
                    <InputField formik={formik} name="phone" label="Phone" type="tel" darkMode={darkMode} />
                    <CheckboxField formik={formik} name="isStudent" label="Student?" darkMode={darkMode} />
                    {formik.values.isStudent && <InputField formik={formik} name="school" label="School Name" darkMode={darkMode} />}
                    <CheckboxField formik={formik} name="isVisitor" label="Visitor?" darkMode={darkMode} />
                    {formik.values.isVisitor && <CheckboxField formik={formik} name="willBeComing" label="Will be coming again?" darkMode={darkMode} />}
                    <InputField formik={formik} name="occupation" label="Occupation" darkMode={darkMode} />
                    <SelectField formik={formik} name="group" label="AG Group" options={["Transformers", "Relentless", "Innovators", "Pacesetters", "Ignition", "Gifted", "Visionaries", "Elevated"]} darkMode={darkMode} />
                    <CheckboxField formik={formik} name="leader" label="Leader?" darkMode={darkMode} />
                    <fieldset className="col-span-1 md:col-span-2 mt-6">
                        <legend className={`text-lg font-medium ${darkMode ? 'text-gray-100' : 'text-gray-800'} mb-4`}>Emergency Contact</legend>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <InputField formik={formik} name="emergencyContact.name" label="Name" darkMode={darkMode} />
                            <InputField formik={formik} name="emergencyContact.phone" label="Phone" type="tel" darkMode={darkMode} />
                            <InputField formik={formik} name="emergencyContact.relation" label="Relation" darkMode={darkMode} />
                        </div>
                    </fieldset>
                    <button
                        type="submit"
                        disabled={formik.isSubmitting}
                        className={`w-full md:col-span-2 py-3 font-semibold rounded-lg transition duration-200 ${darkMode ? 'bg-blue-500 text-white hover:bg-blue-600' : 'bg-blue-600 text-white hover:bg-blue-700'}`}
                    >
                        Register Member
                    </button>
                </form>
            </div>
        </div>
    );
}


const InputField = ({ formik, name, label, type = "text", darkMode }) => (
    <div>
        <label htmlFor={name} className={`block mb-1 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>{label}</label>
        <input
            id={name}
            type={type}
            {...formik.getFieldProps(name)}
            className={`w-full p-3 border rounded-lg ${darkMode ? 'bg-gray-700 text-gray-100 border-gray-600 focus:ring-2 focus:ring-blue-500' : 'bg-white text-gray-900 border-gray-300 focus:ring-2 focus:ring-blue-500'}`}
        />
        {formik.touched[name] && formik.errors[name] && <p className="text-red-500 text-sm">{formik.errors[name]}</p>}
    </div>
);

const CheckboxField = ({ formik, name, label, darkMode }) => (
    <div className="flex items-center">
        <input
            id={name}
            type="checkbox"
            checked={formik.values[name]}
            onChange={formik.handleChange}
            className={`mr-2 h-4 w-4 ${darkMode ? 'text-blue-600' : 'text-blue-600'} focus:ring-blue-500 border-gray-300 rounded`}
        />
        <label htmlFor={name} className={`${darkMode ? 'text-gray-200' : 'text-gray-700'} font-medium`}>{label}</label>
    </div>
);

const SelectField = ({ formik, name, label, options, darkMode }) => (
    <div>
        <label htmlFor={name} className={`block mb-1 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>{label}</label>
        <select
            id={name}
            {...formik.getFieldProps(name)}
            className={`w-full p-3 border rounded-lg ${darkMode ? 'bg-gray-700 text-gray-100 border-gray-600 focus:ring-2 focus:ring-blue-500' : 'bg-white text-gray-900 border-gray-300 focus:ring-2 focus:ring-blue-500'}`}
        >
            <option value="" disabled>Select {label}</option>
            {options.map((option, index) => <option key={index} value={index + 1}>{option}</option>)}
        </select>
        {formik.touched[name] && formik.errors[name] && <p className="text-red-500 text-sm">{formik.errors[name]}</p>}
    </div>
);

const RadioField = ({ formik, name, label, options, darkMode }) => (
    <div>
        <label className={`block mb-1 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>{label}</label>
        <div className="flex items-center space-x-4">
            {options.map((option) => (
                <label key={option} className={`flex items-center ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                    <input
                        type="radio"
                        name={name}
                        value={option}
                        checked={formik.values[name] === option}
                        onChange={formik.handleChange}
                        className={`mr-2 h-4 w-4 ${darkMode ? 'text-blue-600' : 'text-blue-600'} focus:ring-blue-500`}
                    />
                    {option}
                </label>
            ))}
        </div>
    </div>
);

export default MemberForm;
