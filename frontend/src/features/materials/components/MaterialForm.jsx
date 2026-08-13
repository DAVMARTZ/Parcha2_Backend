import { useState } from "react";

const INITIAL_FORM = Object.freeze({
  company_id: "",
  material_type: "",
  quantity: "",
  unit: "kg",
  location: "",
  price: "",
  status_Material: "",
  status: "available",
});

/**
 * Formulario de publicación de materiales.
 */
export default function MaterialForm({ companies, onSubmit }) {
  const [form, setForm] = useState(INITIAL_FORM);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = ({ target }) => {
    setForm((current) => ({
      ...current,
      [target.name]: target.value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);

    const companyId = /^\d+$/.test(form.company_id)
      ? Number(form.company_id)
      : form.company_id;

    try {
      await onSubmit({
        company_id: companyId,
        material_type: form.material_type.trim(),
        quantity: Number(form.quantity),
        unit: form.unit.trim(),
        location: form.location.trim(),
        price: Number(form.price),
        status_Material: form.status_Material.trim(),
        status: form.status,
      });
      setForm(INITIAL_FORM);
    } finally {
      setIsSubmitting(false);
    }
  };

  const formDisabled = isSubmitting || companies.length === 0;

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="material-company" className="form-label">
          Empresa
        </label>
        <select
          id="material-company"
          name="company_id"
          className="form-select"
          value={form.company_id}
          onChange={handleChange}
          required
          disabled={formDisabled}
        >
          <option value="">Seleccione empresa</option>
          {companies.map((company) => (
            <option key={company.id} value={company.id}>
              {company.name}
            </option>
          ))}
        </select>
        {companies.length === 0 && (
          <div className="form-text">
            Registra primero una empresa para publicar materiales.
          </div>
        )}
      </div>

      <div className="mb-3">
        <label htmlFor="material-type" className="form-label">
          Tipo de material
        </label>
        <input
          id="material-type"
          type="text"
          name="material_type"
          className="form-control"
          placeholder="Ej. Cartón, plástico, vidrio"
          value={form.material_type}
          onChange={handleChange}
          required
          disabled={formDisabled}
        />
      </div>

      <div className="row">
        <div className="col-md-6 mb-3">
          <label htmlFor="material-quantity" className="form-label">
            Cantidad
          </label>
          <input
            id="material-quantity"
            type="number"
            name="quantity"
            className="form-control"
            placeholder="Ej. 80"
            value={form.quantity}
            onChange={handleChange}
            min="0.01"
            step="any"
            required
            disabled={formDisabled}
          />
        </div>

        <div className="col-md-6 mb-3">
          <label htmlFor="material-unit" className="form-label">
            Unidad
          </label>
          <input
            id="material-unit"
            type="text"
            name="unit"
            className="form-control"
            placeholder="Ej. kg"
            value={form.unit}
            onChange={handleChange}
            required
            disabled={formDisabled}
          />
        </div>
      </div>

      <div className="mb-4">
        <label htmlFor="material-location" className="form-label">
          Ubicación
        </label>
        <input
          id="material-location"
          type="text"
          name="location"
          className="form-control"
          placeholder="Ciudad o ubicación del material"
          value={form.location}
          onChange={handleChange}
          autoComplete="address-level2"
          required
          disabled={formDisabled}
        />
      </div>

      <div className="mb-4">
        <label htmlFor="material-price" className="form-label">
          Precio
        </label>
        <input
          id="material-price"
          type="number"
          name="price"
          className="form-control"
          placeholder="Precio del material"
          value={form.price}
          onChange={handleChange}
          required
          disabled={formDisabled}
        />
      </div>

      <div className="mb-4">
        <label htmlFor="material-status" className="form-label">
          Estado del material
        </label>
        <input
          id="material-status"
          type="text"
          name="status_Material"
          className="form-control"
          placeholder="Estado del material"
          value={form.status_Material}
          onChange={handleChange}
          required
          disabled={formDisabled}
        />
      </div>

      <div className="d-grid">
        <button type="submit" className="btn btn-success" disabled={formDisabled}>
          {isSubmitting ? "Creando…" : "Crear publicación"}
        </button>
      </div>
    </form>
  );
}
