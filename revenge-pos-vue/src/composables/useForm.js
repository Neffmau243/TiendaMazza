// composables/useForm.js
import { reactive, computed } from 'vue'

export function useForm(initialValues, validationRules = {}) {
  const values = reactive({ ...initialValues })
  const errors = reactive({})
  const touched = reactive({})

  const validate = (field) => {
    if (!validationRules[field]) return true

    const rules = validationRules[field]
    const value = values[field]

    for (const rule of rules) {
      const result = rule(value)
      if (result !== true) {
        errors[field] = result
        return false
      }
    }

    delete errors[field]
    return true
  }

  const validateAll = () => {
    let isValid = true
    for (const field in validationRules) {
      if (!validate(field)) {
        isValid = false
      }
    }
    return isValid
  }

  const touch = (field) => {
    touched[field] = true
  }

  const reset = () => {
    Object.assign(values, initialValues)
    Object.keys(errors).forEach(key => delete errors[key])
    Object.keys(touched).forEach(key => delete touched[key])
  }

  const setValues = (newValues) => {
    Object.assign(values, newValues)
  }

  const setValue = (field, value) => {
    values[field] = value
  }

  const isValid = computed(() => Object.keys(errors).length === 0)

  return {
    values,
    errors,
    touched,
    isValid,
    validate,
    validateAll,
    touch,
    reset,
    setValues,
    setValue
  }
}
