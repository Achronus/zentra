import styles from "./form.module.css";

type FormTitleProps = {
  title: string;
  desc: string;
};

type FormSectionProps = {
  title: string;
  children: React.ReactNode;
};

export const FormTitle = ({ title, desc }: FormTitleProps) => {
  return (
    <section className={styles.section}>
      <h1 className={styles.title}>{title}</h1>
      <p className={styles.desc}>{desc}</p>
    </section>
  );
};

export const FormSection = ({ title, children }: FormSectionProps) => {
  return (
    <section className={styles.section}>
      <div className={styles.titleContainer}>
        <h2 className={styles.sectionTitle}>{title}</h2>
      </div>
      {children}
    </section>
  );
};

export const FormRow = ({ children }: { children: React.ReactNode }) => {
  return <div className={styles.row}>{children}</div>;
};
